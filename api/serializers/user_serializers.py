"""User Serializers"""

from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework_simplejwt.tokens import RefreshToken

# DRF Simple JWT: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/customizing_token_claims.html
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150, allow_blank=True, allow_null=True)
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField()
    #is_admin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff',)

    """ def get_is_admin(self, obj):
        print('user_obj:', obj)
        return obj.is_staff """

    def create(self, validated_data):
        return User.objects.create(**validated_data)

class UserSerializerWithToken(UserSerializer):
    """
    Inherits from UserSerializer and includes a create method for registering new users.
    """
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'token',)

    def get_token(self, user_obj):
        token = RefreshToken.for_user(user_obj)
        return str(token.access_token)

    def create(self, validated_data):
        """Adds create functionality for the User model."""
        return User.objects.all().create(**validated_data)




"""
JWT Custom Serializer
DRF Simple JWT: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/customizing_token_claims.html
"""
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        """Adds non-encoded data to the token."""
        data = super().validate(attrs)

        # Get the fields from the user profile serializer.
        serializer = UserSerializerWithToken(self.user).data

        for fields, values in serializer.items():
            data[fields] = values

        return data