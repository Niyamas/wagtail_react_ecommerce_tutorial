"""Cart Serializers"""

from users.models import ShippingAddress
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from api.serializers.user_serializers import UserSerializer

from users.models import Cart, Order
from items.models import ItemDetailPage


class ShippingAddressSerializer(serializers.Serializer):
    """Shipping address serializer."""

    id = serializers.IntegerField(read_only=True)
    cart = PrimaryKeyRelatedField(queryset=Cart.objects.all())
    address = serializers.CharField(max_length=200)
    city = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=10, required=False)
    country = serializers.CharField(max_length=100)

class OrderSerializer(serializers.Serializer):
    """Order serializer."""

    id = serializers.IntegerField(read_only=True)
    item = PrimaryKeyRelatedField(queryset=ItemDetailPage.objects.all())
    image = serializers.CharField(max_length=2000)
    cart = PrimaryKeyRelatedField(queryset=Cart.objects.all())
    name = serializers.CharField(max_length=200)
    quantity = serializers.IntegerField(min_value=0)
    price = serializers.DecimalField(max_digits=7, decimal_places=2)

    def create(self, validated_data):
        """
        Adds create write functionality to the cart serializer
        """
        return Order.objects.create(**validated_data)

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