from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,

    GenericAPIView
)

from api.serializers import (
    ReviewSerializer,
    ItemSerializer,

    UserSerializer,
    UserSerializerWithToken
)

from .products import products

from items.models import (
    ItemListingPage,
    ItemDetailPage,
    ItemCategory,
)

from users.models import (
    Review,
    Cart,
    Order,
    ShippingAddress
)

# DRF Simple JWT: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/customizing_token_claims.html
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


@api_view(['GET'])
def getRoutes(request):
    """
    API v1 home page.
    """
    routes = {
        'Item list': '/api/v1/items/',
        'Item details': '/api/v1/item/<int:pk>/',

        'JWT': '/api/v1/users/login/',
    }

    return Response(routes)


class ItemListView(ListAPIView):
    """
    Lists all of the items. Can get this in Wagtail API, but that is read-only.

    Add a get_queryset method to create parameters for the URL to filter the list of items.
    """
    serializer_class = ItemSerializer
    queryset = ItemDetailPage.objects.all()


class ItemDetailListView(RetrieveUpdateDestroyAPIView):
    """
    """
    serializer_class = ItemSerializer
    queryset = ItemDetailPage.objects.all()






@api_view(['GET'])
def getUserProfile(request):
    """
    Needs the JWT token to be passed in order to return the serialized data.
    That is, the user needs to be logged in to access his/her profile data.
    """
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)



""" class UserProfileView(GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_current_user(self):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return request.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context = ['user']
        return context """








# Simple JWT serializers
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        """Adds non-encoded data to the token."""
        data = super().validate(attrs)

        # Get the fields from the user profile serializer.
        serializer = UserSerializerWithToken(self.user).data

        for fields, values in serializer.items():
            data[fields] = values

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer