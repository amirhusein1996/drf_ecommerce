from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.views import extend_schema
from .serializers import (
    BillingAddressModelSerializer,
    ShippingAddressModelSerializer
    )
from .models import (
    BillingAddress,
    ShippingAddress
    )


@extend_schema(tags=['Billing Address'])
class BillingAddressModelViewSet(ModelViewSet):
    """
    ## Viewset for managing billing addresses.

    - Provides CRUD operations for the BillingAddress model, restricted to the
        current authenticated user. Only authenticated users can access these views.
    """

    serializer_class = BillingAddressModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return the queryset of ShippingAddress objects belonging to the current user
        """
        return BillingAddress.objects.filter(
            user=self.request.user
        )


@extend_schema(tags=['Shipping Address'])
class ShippingAddressModelViewSet(ModelViewSet):

    """
    ## Viewset for managing shipping addresses.

    - Provides CRUD operations for the ShippingAddress model, restricted to the
        current authenticated user. Only authenticated users can access these views.
    """

    serializer_class = ShippingAddressModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return the queryset of ShippingAddress objects belonging to the current user
        """
        return ShippingAddress.objects.filter(
            user=self.request.user
        )
