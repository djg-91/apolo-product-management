from django.urls import URLPattern, path
from .views import OrderListCreateView, OrderDetailDeleteView


# Define the URL patterns for the order-related endpoints.
urlpatterns: list[URLPattern] = [
    # Endpoint to list all orders or create a new order.
    path('', OrderListCreateView.as_view(), name='order-list-create'),

    # Endpoint to retrieve or delete a specific order by its primary key (order_id).
    path('<int:pk>/', OrderDetailDeleteView.as_view(), name='product-detail-delete'),
]
