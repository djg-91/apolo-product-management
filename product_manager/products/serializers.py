from rest_framework import serializers
from .models import Product


class ErrorSerializer(serializers.Serializer):
    """
    Serializer for error messages.
    Used to standardize error responses in the API.
    """
    error: serializers.CharField = serializers.CharField()


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for individual products.
    """
    class Meta:
        model: type[Product] = Product
        fields: list[str] = ['id', 'name', 'price', 'stock']
