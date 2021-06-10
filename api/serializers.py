from django.contrib.auth.models import User


from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from rest_framework_simplejwt.tokens import RefreshToken

from wagtail.search import queryset

from users.models import (
    Review,
    Cart,
    Order,
    ShippingAddress
)
from items.models import (
    ItemListingPage,
    ItemDetailPage,
    ItemCategory,
)


"""User Serializers"""
class ReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        read_only=True
    )
    item = PrimaryKeyRelatedField(
        read_only=True,
        #queryset=ItemDetailPage.objects.all()
    )
    user = PrimaryKeyRelatedField(
        read_only=True,
        #queryset=User.objects.all()
    )
    name = serializers.CharField(
        read_only=True
    )
    rating = serializers.IntegerField(
        read_only=True
    )
    comment = serializers.CharField(
        read_only=True,
        max_length=2000,
        required=False,
        allow_blank=True
    )




class UserSerializer(serializers.Serializer):
    """
    Specify the user serializer fields for logged in users (JWT's tokens)
    """
    id = serializers.IntegerField(
        read_only=True
    )
    username = serializers.CharField(
        #read_only=True,
        max_length=150
    )
    email = serializers.EmailField(
        #read_only=True,
    )
    #name = serializers.SerializerMethodField(
    #    read_only=True
    #)
    first_name = serializers.CharField(
        max_length=150
    )
    last_name = serializers.CharField(
        max_length=150,
        required=False
    )
    is_admin = serializers.SerializerMethodField(
        read_only=True
    )

    #def get_name(self, user_obj):
    #    name = user_obj.first_name
    #    if name == '':
    #        name = user_obj.email
        
    #    return name

    def get_is_admin(self, user_obj):
        return user_obj.is_staff
    
class UserSerializerWithToken(UserSerializer):
    """
    Inherits from UserSerializer and includes a create method for registering new users.
    """
    username = serializers.CharField(
        max_length=150
    )
    email = serializers.EmailField()
    #name = serializers.SerializerMethodField()
    first_name = serializers.CharField(
        max_length=150
    )
    last_name = serializers.CharField(
        max_length=150,
        required=False
    )
    token = serializers.SerializerMethodField()

    def get_token(self, user_obj):
        token = RefreshToken.for_user(user_obj)
        return str(token.access_token)

    def create(self, validated_data):
        """Adds create functionality for the User model."""
        return User.objects.all().create(**validated_data)



"""Item Serializers."""
class ImageSerializer(serializers.Serializer):
    """Nested image serializer included in the ItemDetailSerializer."""

    title = serializers.CharField(read_only=True)
    file = serializers.ImageField(read_only=True)


class ItemSerializer(serializers.Serializer):
    """Item serializer for various views like list and detail."""

    id = serializers.IntegerField(
        read_only=True
    )
    title = serializers.CharField(
        read_only=True,
        max_length=255
    )
    user = PrimaryKeyRelatedField(
        read_only=True,
        #queryset=User.objects.all()
    )
    image = ImageSerializer(
        read_only=True
    )
    category = PrimaryKeyRelatedField(
        read_only=True,
        #queryset=ItemCategory.objects.all()
    )
    brand = serializers.CharField(
        read_only=True,
        max_length=200
    )
    description = serializers.CharField(
        read_only=True,
        max_length=2000
    )
    price = serializers.DecimalField(
        read_only=True,
        max_digits=7,
        decimal_places=2
    )
    quantity_in_stock = serializers.IntegerField(
        read_only=True
    )
    rating = serializers.DecimalField(
        read_only=True,
        max_digits=7,
        decimal_places=2
    )
    quantity_reviews = serializers.IntegerField(
        read_only=True
    )

class ShippingAddressSerializer(serializers.Serializer):
    """"""

    cart = PrimaryKeyRelatedField(
        #read_only=True,
        queryset=ShippingAddress.objects.all()
    )
    address = serializers.CharField(
        max_length=200
    )
    city = serializers.CharField(
        max_length=100
    )
    postal_code = serializers.CharField(
        max_length=10,
        required=False
    )
    country = serializers.CharField(
        max_length=100
    )
    shipping_price = serializers.DecimalField(
        max_digits=7,
        decimal_places=2
    )

    def create(self, validated_data):
        """
        Adds create write functionality to the cart serializer
        """
        return ShippingAddress.objects.create(**validated_data)

class OrderSerializer(serializers.Serializer):
    """"""

    item = PrimaryKeyRelatedField(
        #read_only=True,
        #queryset=ItemListingPage.live().public()
        queryset=ItemListingPage.objects.all()
    )
    image = serializers.CharField(
        max_length=2000
    )
    cart = PrimaryKeyRelatedField(
        #read_only=True,
        queryset=Order.objects.all()
    )
    name = serializers.CharField(
        max_length=200
    )
    quantity = serializers.IntegerField(
        min_value=0
    )
    price = serializers.DecimalField(
        max_digits=7,
        decimal_places=2
    )

    def create(self, validated_data):
        """
        Adds create write functionality to the cart serializer
        """
        return Order.objects.create(**validated_data)

"""Cart Serializers"""
class CartSerializer(serializers.Serializer):
    """Cart serializer."""

    user = PrimaryKeyRelatedField(
        #read_only=True,
        queryset=User.objects.all()
    )
    orders = serializers.SerializerMethodField(
        read_only=True
    )
    shipping_address = serializers.SerializerMethodField(
        read_only=True
    )
    payment_method = serializers.CharField(
        max_length=100
    )
    tax_price = serializers.DecimalField(
        max_digits=7,
        decimal_places=2
    )
    shipping_price = serializers.DecimalField(
        max_digits=7,
        decimal_places=2
    )
    total_price = serializers.DecimalField(
        max_digits=7,
        decimal_places=2
    )
    is_paid = serializers.BooleanField(
        required=False
    )
    paid_at = serializers.DateTimeField(
        required=False
    )
    is_delivered = serializers.BooleanField(
        required=False
    )
    delivered_at = serializers.DateTimeField(
        required=False
    )
    created_at = serializers.DateTimeField(
        required=False
    )

    def get_user(self, obj):
        """Returns the user data. Obj = user object?"""
        user = obj.user
        serializer = UserSerializer(data=user, many=False)
        return serializer.data

    def get_orders(self, obj):
        """Returns the customer's orders in their cart. Obj = orders object?"""
        items = obj.order_set.all()
        serializer = OrderSerializer(data=items, many=True)
        return serializer.data

    def get_shipping_address(self, obj):
        """Returns the customer's shipping address if it exists. Obj = shipping_address obj?"""
        try:
            address = ShippingAddressSerializer(data=obj.shipping_address, many=False)
        except:
            address = False

        return address

    def create(self, validated_data):
        """
        Adds create write functionality to the cart serializer
        """
        return Cart.objects.create(**validated_data)