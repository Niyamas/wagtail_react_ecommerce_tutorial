"""Cart Serializers"""

from users.models import ShippingAddress
from django.contrib.auth.models import User

from rest_framework import serializers

from api.serializers import (
    UserSerializer
)

from users.models import (
    Cart
)

class ShippingAddressSerializer(serializers.Serializer):
    """Shipping address serializer."""

class OrderSerializer(serializers.Serializer):
    """Order serializer."""

class CartSerializer(serializers.Serializer):
    """Cart serializer."""

    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(many=False)
    orders = OrderSerializer(many=True)
    ShippingAddress = ShippingAddressSerializer(many=False)
    payment_method = serializers.CharField(max_length=100)
    shipping_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    tax_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    is_paid = serializers.BooleanField(required=False)
    paid_at = serializers.DateTimeField(required=False)
    is_delivered = serializers.BooleanField(required=False)
    delivered_at = serializers.DateTimeField(required=False)
    created_at = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        """
        Adds create write functionality to the cart serializer
        """
        return Cart.objects.create(**validated_data)