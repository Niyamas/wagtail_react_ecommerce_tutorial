"""Item Serializers"""

from django.contrib.auth.models import User

from users.models import Review
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from users.models import (
    Review
)
from items.models import ItemDetailPage

class ReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    item = PrimaryKeyRelatedField(queryset=ItemDetailPage.objects.all())
    user = PrimaryKeyRelatedField(queryset=User.objects.all())
    name = serializers.CharField()
    rating = serializers.IntegerField()
    comment = serializers.CharField(max_length=2000, required=False, allow_blank=True)
    created_at = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        """Adds create functionality to the Review model."""
        return Review.objects.all().create(**validated_data)

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
    review_data = serializers.SerializerMethodField(read_only=True)

    def get_review_data(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data