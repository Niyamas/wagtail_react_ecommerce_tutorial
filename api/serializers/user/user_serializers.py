"""User Serializers"""

from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import (
    Review
)


class ReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    item = PrimaryKeyRelatedField(read_only=True)
    user = PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(read_only=True)
    rating = serializers.IntegerField(read_only=True)
    comment = serializers.CharField(read_only=True, max_length=2000, required=False, allow_blank=True)

class UserSerializer(serializers.Serializer):
    """
    Specify the user serializer fields for logged in users (JWT's tokens)
    """
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    #name = serializers.SerializerMethodField(
    #    read_only=True
    #)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150, required=False)
    is_admin = serializers.SerializerMethodField(read_only=True)

    def get_is_admin(self, user_obj):
        return user_obj.is_staff

class UserSerializerWithToken(UserSerializer):
    """
    Inherits from UserSerializer and includes a create method for registering new users.
    """
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150, required=False)
    token = serializers.SerializerMethodField()

    def get_token(self, user_obj):
        token = RefreshToken.for_user(user_obj)
        return str(token.access_token)

    def create(self, validated_data):
        """Adds create functionality for the User model."""
        return User.objects.all().create(**validated_data)