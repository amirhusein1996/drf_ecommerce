from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BillingAddressModelViewSet, ShippingAddressModelViewSet


app_name = 'addresses'

router = DefaultRouter()
router.register('billing-addresses', BillingAddressModelViewSet, )
router.register('shipping-addresses', ShippingAddressModelViewSet)

urlpatterns = router.urls
