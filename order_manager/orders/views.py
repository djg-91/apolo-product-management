import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer, ErrorSerializer
from drf_spectacular.utils import extend_schema

PRODUCT_API_BASE = 'http://127.0.0.1:8000/api/products/'

class OrderListCreateView(APIView):
    @extend_schema(
        summary='Retrieve all orders',
        description='Fetches a list of all existing orders with their details.',
        tags=['Orders'],
        responses={200: OrderSerializer(many=True)},
    )
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
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
    def post(self, request):
        items = request.data.get('items', [])
        if not items:
            return Response({'error': 'No items provided'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create()

        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity')

            if not product_id or not quantity:
                order.delete()
                return Response({'error': 'Invalid item data'}, status=status.HTTP_400_BAD_REQUEST)

            product_response = requests.get(f'{PRODUCT_API_BASE}{product_id}/')
            if product_response.status_code != 200:
                order.delete()
                return Response({'error': f'Product {product_id} not found'}, status=status.HTTP_404_NOT_FOUND)

            product_data = product_response.json()
            if product_data['stock'] < quantity:
                order.delete()
                return Response(
                    {'error': f'Insufficient stock for product {product_id}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            stock_update_response = requests.patch(
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

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
