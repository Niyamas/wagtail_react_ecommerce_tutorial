"""Item Serializers"""

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField


class ImageSerializer(serializers.Serializer):
    """Nested image serializer included in the ItemDetailSerializer."""

    title = serializers.CharField(read_only=True)
    file = serializers.ImageField(read_only=True)

class ItemSerializer(serializers.Serializer):
    """Item serializer for various views like list and detail."""

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True, max_length=255)
    user = PrimaryKeyRelatedField(read_only=True)
    image = ImageSerializer(read_only=True)
    category = PrimaryKeyRelatedField(read_only=True)
    brand = serializers.CharField(read_only=True, max_length=200)
    description = serializers.CharField(read_only=True, max_length=2000)
    price = serializers.DecimalField(read_only=True, max_digits=7, decimal_places=2)
    quantity_in_stock = serializers.IntegerField()
    rating = serializers.DecimalField(read_only=True, max_digits=7, decimal_places=2)
    quantity_reviews = serializers.IntegerField(read_only=True)