from django.urls import URLPattern, path
from .views import OrderListCreateView


urlpatterns: list[URLPattern] = [
    path('', OrderListCreateView.as_view(), name='order-list-create'),
]
