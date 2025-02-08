from django.db import models


class Order(models.Model):
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order: models.ForeignKey = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_id: models.IntegerField = models.IntegerField()
    quantity: models.PositiveIntegerField = models.PositiveIntegerField()
    price: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
