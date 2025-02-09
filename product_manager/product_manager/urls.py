from django.contrib import admin
from django.urls import URLPattern, path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns: list[URLPattern] = [
    path('admin/', admin.site.urls),
    path('api/products/', include('products.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
