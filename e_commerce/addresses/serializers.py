from rest_framework import serializers
from .models import BillingAddress, ShippingAddress


class BillingAddressModelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = BillingAddress
        fields = "__all__"
        read_only_fields = ('id', 'user')


class ShippingAddressModelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = ShippingAddress
        fields = "__all__"
        read_only_fields = ('id', 'user')
