from django.urls import path
from .views import ProductListCreateView, ProductStockUpdateView, ProductDetailView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/stock/', ProductStockUpdateView.as_view(), name='product-stock-update'),
]
