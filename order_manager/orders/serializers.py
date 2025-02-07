from rest_framework import serializers
from .models import Order, OrderItem

class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'items', 'total_price']

    def get_total_price(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())
