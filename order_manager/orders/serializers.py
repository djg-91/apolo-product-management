from rest_framework import serializers
from .models import Order, OrderItem


class ErrorSerializer(serializers.Serializer):
    """
    Serializer for error messages.
    Used to standardize error responses in the API.
    """
    error: serializers.CharField = serializers.CharField()


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for individual order items.
    """
    class Meta:
        model: type[OrderItem] = OrderItem
        fields: list[str] = ['product_id', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for orders.
    Handles nested serialization for order items and calculates the total price of an order.
    """
    def get_total_price(self, obj: Order) -> float:
        """
        Calculate the total price of an order.

        The total price is calculated by summing the product of 
        the price and quantity for each item in the order.

        Args:
            obj (Order): The order instance being serialized.

        Returns:
            float: The total price of the order.
        """
        return sum(item.price * item.quantity for item in obj.items.all())
    
    items: list[OrderItemSerializer] = OrderItemSerializer(many=True)
    total_price: serializers.SerializerMethodField = serializers.SerializerMethodField()

    class Meta:
        model: type[Order] = Order
        fields: list[str] = ['id', 'created_at', 'items', 'total_price']
