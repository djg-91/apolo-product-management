from django.urls import URLPattern, path
from .views import ProductListCreateView, ProductStockUpdateView, ProductDetailDeleteView

# Define the URL patterns for the product-related endpoints.
urlpatterns: list[URLPattern] = [
    # Endpoint to list all products or create a new product.
    path('', ProductListCreateView.as_view(), name='product-list-create'),

    # Endpoint to retrieve or delete a specific product identified by its primary key (product_id).
    path('<int:pk>/', ProductDetailDeleteView.as_view(), name='product-detail-delete'),

    # Endpoint to update the stock of a specific product identified by its primary key (product_id).
    path('<int:pk>/stock/', ProductStockUpdateView.as_view(), name='product-stock-update'),
]
