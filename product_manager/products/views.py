from typing import Optional
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer, ErrorSerializer
from drf_spectacular.utils import extend_schema


class ProductListCreateView(APIView):
    """
    Handles listing all products and creating new products.
    """
    serializer_class = ProductSerializer
    
    @extend_schema(
        summary='List all products',
        description='Returns a list of all available products.',
        tags=['Products'],
        responses={
            200: ProductSerializer(many=True),
        },
    )
    def get(self, request: Request) -> Response:
        """ 
        Retrieves a list of all products.

        Returns:
            Response: A Response object containing the serialized list of products.
        """
        products: list[Product] = Product.objects.all()
        serializer: ProductSerializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


    @extend_schema(
        summary='Create a new product',
        description='Creates a new product using the provided data in the request body.',
        tags=['Products'],
        responses={
            201: ProductSerializer,
            400: ErrorSerializer,
        },
    )
    def post(self, request: Request) -> Response:
        """
        Creates a new product after validating the input data.

        Args:
            request (Request): The Request object containing the product data.

        Returns:
            Response: A Response object containing the serialized product created or validation errors.
        """
        serializer: ProductSerializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailDeleteView(APIView):
    """
    Handles retrieving and deleting a specific product by its ID.
    """
    @extend_schema(
        summary='Get product details',
        description='Returns detailed information about a product identified by its ID.',
        tags=['Products'],
        responses={
            200: ProductSerializer,
            404: ErrorSerializer,
        },
    )
    def get(self, request: Request, pk: int) -> Response:
        """
        Retrieves the details of a specific product by its primary key (ID).

        Args:
            pk (int): The primary key of the product.

        Returns:
            Response: A Response object containing the serialized product or an error message if the product does not exist.
        """
        try:
            product: Product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer: ProductSerializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @extend_schema(
        summary='Delete a product',
        description='Deletes a product identified by its ID.',
        tags=['Products'],
        responses={
            204: None,
            404: ErrorSerializer,
        },
    )
    def delete(self, request: Request, pk: int) -> Response:
        """
        Deletes a specific product by its primary key (ID).

        Args:
            pk (int): The primary key of the product.

        Returns:
            Response: A Response object with status 204 if the product was deleted successfully, or an error message if the product does not exist.
        """
        try:
            product: Product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ProductStockUpdateView(APIView):
    """
    Handles updating the stock of a specific product by its ID.
    """
    @extend_schema(
        summary='Update product stock',
        description=(
            'Updates the stock of a product identified by its ID. '
            'The request body must include the `stock` field with a non-negative integer value.'
        ),
        tags=['Products'],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'stock': {
                        'type': 'integer',
                        'description': 'New stock value for the product',
                    },
                },
                'required': ['stock'],
            },
        },
        responses={
            200: ProductSerializer,
            400: ErrorSerializer,
            404: ErrorSerializer,
        },
    )
    def patch(self, request: Request, pk: int) -> Response:
        """
        Updates the stock of a specific product by its primary key (ID).

        Args:
            request (Request): The Request object containing the new stock value.
            pk (int): The primary key of the product.

        Returns:
            Response: A Response object containing the updated product data, or an error message if the product does not exist
                      or the stock value is invalid.
        """
        try:
            product: Product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        stock: Optional[int] = request.data.get('stock')

        try:
            stock = int(stock)
            if stock < 0:
                return Response({'error': 'Stock cannot be negative'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError):
            return Response({'error': 'Stock must be a valid integer'}, status=status.HTTP_400_BAD_REQUEST)

        product.stock = stock
        product.save()
        serializer: ProductSerializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
