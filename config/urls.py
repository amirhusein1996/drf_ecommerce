from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # local apps
    path('api/users/', include('e_commerce.users.urls', namespace='users')),
    path('api/', include('e_commerce.products.urls', namespace='products')),
    path('api/', include('e_commerce.addresses.urls', namespace='addresses')),
    path('api/', include('e_commerce.coupon.urls', namespace='coupon')),
    path('api/', include('e_commerce.orders.urls', namespace='orders')),

]
