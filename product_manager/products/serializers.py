from rest_framework import serializers
from .models import Product

class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock']
