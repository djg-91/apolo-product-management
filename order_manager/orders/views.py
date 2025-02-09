from collections import defaultdict
from typing import Union, Tuple, Optional
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from .models import Order, OrderItem
from .serializers import OrderSerializer, ErrorSerializer
from drf_spectacular.utils import extend_schema

PRODUCT_API_BASE: str = 'http://127.0.0.1:8000/api/products/'


def validate_and_group_items(items: list[dict[str, int]]) -> Union[Tuple[dict[int, int], None], Tuple[None, str]]:
    """
    Validates each item in an order and groups products by their IDs, summing their quantities.

    Args:
        items (list[dict[str, int]]): A list of items, where each item is a dictionary containing
                                      'product_id' and 'quantity'.

    Returns:
        Union[Tuple[dict[int, int], None], Tuple[None, str]]: A tuple containing:
            - A dictionary with product IDs as keys and their total quantities as values.
            - An error message if validation fails, otherwise None.
    """
    grouped_items: defaultdict[int, int] = defaultdict(int)

    for item in items:
        product_id: Optional[int] = item.get('product_id')
        quantity: Optional[int] = item.get('quantity')

        if product_id is None or quantity is None:
            return None, "Each item must contain 'product_id' and 'quantity'."

        try:
            product_id = int(product_id)
            quantity = int(quantity)
        except (TypeError, ValueError):
            return None, "'product_id' and 'quantity' must be valid integers."

        if product_id < 0 or quantity < 0:
            return None, "'product_id' and 'quantity' must be non-negative."

        grouped_items[product_id] += quantity

    return dict(grouped_items), None


class OrderListCreateView(APIView):
    """
    Handles listing all orders and creating new orders.
    """
    @extend_schema(
        summary='List all orders',
        description='Returns a list of all available orders with their details.',
        tags=['Orders'],
        responses={200: OrderSerializer(many=True)},
    )
    def get(self, request: Request) -> Response:
        """
        Retrieves a list of all orders.

        Returns:
            Response: A Response object containing the serialized list of orders.
        """
        orders: list[Order] = Order.objects.all()
        serializer: OrderSerializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


    @extend_schema(
        summary='Create a new order',
        description=(
            'Creates a new order and validates product availability and stock. '
            'Deducts the appropriate stock from the product inventory and adds the order items.'
        ),
        tags=['Orders'],
        request={
            'application/json': {
                'example': {
                    'items': [
                        {'product_id': 1, 'quantity': 2},
                        {'product_id': 3, 'quantity': 1}
                    ]
                }
            }
        },
        responses={
            201: OrderSerializer(),
            400: ErrorSerializer,
            404: ErrorSerializer,
        },
    )
    def post(self, request: Request) -> Response:
        """
        Creates a new order after validating items, checking product availability, and updating stock.

        Args:
            request (Request): The Request object containing the order data.

        Returns:
            Response: A Response object containing the serialized order created or validation errors.
        """
        items: Optional[list[dict[str, int]]] = request.data.get('items', [])
        if not items:
            return Response({'error': 'No items provided'}, status=status.HTTP_400_BAD_REQUEST)

        grouped_items, error = validate_and_group_items(items)

        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        order: Order = Order.objects.create()

        for product_id, quantity in grouped_items.items():
            # Fetch product details from the Product Manager API
            product_response: requests.Response = requests.get(f'{PRODUCT_API_BASE}{product_id}/')
            if product_response.status_code != 200:
                order.delete()
                return Response({'error': f'Product {product_id} not found'}, status=status.HTTP_404_NOT_FOUND)

            product_data: dict[str, Union[str, int, float]] = product_response.json()

            # Ensure that the total quantity does not exceed the available stock
            if product_data['stock'] < quantity:
                order.delete()
                return Response(
                    {'error': f'Insufficient stock for product {product_id}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Update product stock
            stock_update_response: requests.Response = requests.patch(
                f'{PRODUCT_API_BASE}{product_id}/stock/',
                data={'stock': product_data['stock'] - quantity}
            )

            if stock_update_response.status_code != 200:
                order.delete()
                return Response(
                    {'error': f'Failed to update stock for product {product_id}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            OrderItem.objects.create(
                order=order,
                product_id=product_id,
                quantity=quantity,
                price=product_data['price']
            )

        serializer: OrderSerializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class OrderDetailDeleteView(APIView):
    """
    Handles retrieving and deleting a specific order by its ID.
    """
    @extend_schema(
        summary='Get order details',
        description='Returns detailed information about an order identified by its ID.',
        tags=['Orders'],
        responses={
            200: OrderSerializer,
            404: ErrorSerializer,
        },
    )
    def get(self, request: Request, pk: int) -> Response:
        """
        Retrieves the details of a specific order by its primary key (ID).

        Args:
            pk (int): The primary key of the order.

        Returns:
            Response: A Response object containing the serialized order or an error message if the order does not exist.
        """
        try:
            product: Order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer: OrderSerializer = OrderSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @extend_schema(
        summary='Delete an order',
        description='Deletes an order identified by its ID.',
        tags=['Orders'],
        responses={
            204: None,
            404: ErrorSerializer,
        },
    )
    def delete(self, request: Request, pk: int) -> Response:
        """
        Deletes a specific order by its primary key (ID).

        Args:
            pk (int): The primary key of the order.

        Returns:
            Response: A Response object with status 204 if the order was deleted successfully, or an error message if the order does not exist.
        """
        try:
            order: Order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    