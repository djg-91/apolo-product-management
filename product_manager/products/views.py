from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer, ErrorSerializer
from drf_spectacular.utils import extend_schema

class ProductDetailView(APIView):
    @extend_schema(
        summary='Get product details',
        description='Returns detailed information about a product by its ID.',
        tags=['Products'],
        responses={
            200: ProductSerializer,
            404: ErrorSerializer,
        },
    )
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductListCreateView(APIView):
    serializer_class = ProductSerializer
    
    @extend_schema(
        summary='List all products',
        description='Returns a list of all products.',
        tags=['Products'],
        responses={
            200: ProductSerializer(many=True),
        },
    )
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary='Create a new product',
        description='Creates a new product with the provided data.',
        tags=['Products'],
        responses={
            201: ProductSerializer,
            400: ErrorSerializer,
        },
    )
    def post(self, request):
        
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductStockUpdateView(APIView):
    @extend_schema(
        summary='Update product stock',
        description=(
            'Updates the stock of a product by its ID. '
            'Requires the `stock` field in the request body.'
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
    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        stock = request.data.get('stock')

        try:
            stock = int(stock)
            if stock < 0:
                return Response({'error': 'Stock cannot be negative'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError):
            return Response({'error': 'Stock must be a valid integer'}, status=status.HTTP_400_BAD_REQUEST)

        product.stock = stock
        product.save()
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)