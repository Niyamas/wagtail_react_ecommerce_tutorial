"""Cart Serializers"""

from users.models import ShippingAddress
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from api.serializers.user_serializers import UserSerializer

from users.models import Cart, Order, ShippingAddress
from items.models import ItemDetailPage


class ShippingAddressSerializer(serializers.Serializer):
    """Shipping address serializer."""

    id = serializers.IntegerField(read_only=True)
    cart = PrimaryKeyRelatedField(queryset=Cart.objects.all())
    address = serializers.CharField(max_length=200)
    city = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=10, required=False)
    country = serializers.CharField(max_length=100)

    def create(self, validated_data):
        """
        Adds create write functionality to the cart serializer
        """
        return ShippingAddress.objects.create(**validated_data)

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


from django.forms.models import model_to_dict

class CartSerializer(serializers.Serializer):
    """Cart serializer."""

    id = serializers.IntegerField(read_only=True)
    user = PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    user_data = serializers.SerializerMethodField(read_only=True)
    orders = serializers.SerializerMethodField(read_only=True)
    shipping_address_data = serializers.SerializerMethodField(read_only=True)
    payment_method = serializers.CharField(max_length=100, required=False)
    shipping_price = serializers.DecimalField(max_digits=7, decimal_places=2, required=False)
    tax_price = serializers.DecimalField(max_digits=7, decimal_places=2, required=False)
    #items_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=7, decimal_places=2, required=False)
    is_paid = serializers.BooleanField(required=False)
    paid_at = serializers.DateTimeField(required=False, allow_null=True)
    is_delivered = serializers.BooleanField(required=False)
    delivered_at = serializers.DateTimeField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(required=False)

    def get_user_data(self, obj):
        user = model_to_dict(obj.user)
        serializer = UserSerializer(data=user, many=False)
        serializer.is_valid()
        return serializer.data

    def get_orders(self, obj):
        items = obj.order_set.all()
        serializer = OrderSerializer(data=items, many=True)
        serializer.is_valid()
        return serializer.data

    def get_shipping_address_data(self, obj):
        try:
            address = model_to_dict(obj.shippingaddress)
            serializer = ShippingAddressSerializer(data=address, many=False)
            serializer.is_valid()
            serializer = serializer.data
        except:
            serializer = False
        return serializer

    def create(self, validated_data):
        """
        Adds create write functionality to the cart serializer
        """
        return Cart.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.is_paid = validated_data.get('is_paid', instance.is_paid)
        instance.paid_at = validated_data.get('paid_at', instance.paid_at)
        instance.save()
        return instance