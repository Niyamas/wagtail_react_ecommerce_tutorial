from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
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
from django.contrib.auth.models import User

### User Serializers
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
        allow_blank=True)







class ImageSerializer(serializers.Serializer):
    """Nested image serializer included in the ItemDetailSerializer."""

    title = serializers.CharField(read_only=True)
    file = serializers.ImageField(read_only=True)


class ItemSerializer(serializers.Serializer):
    """"""

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