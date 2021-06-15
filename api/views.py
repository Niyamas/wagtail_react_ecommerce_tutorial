from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.forms.models import model_to_dict

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

# DRF Simple JWT: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/customizing_token_claims.html
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    CreateAPIView,
)

from api.serializers.user_serializers import (
    ReviewSerializer,
    UserSerializer,
    UserSerializerWithToken
)

from api.serializers.item_serializers import (
    ItemSerializer
)

from api.serializers.cart_serializers import (
    ShippingAddressSerializer,
    OrderSerializer,
    CartSerializer
)

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


"""Home API View"""
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


"""Item API Views"""

class ItemListView(ListAPIView):
    """
    Lists all of the items. Can get this in Wagtail API, but that is read-only.
    Add a get_queryset method to create parameters for the URL to filter the list of items.
    @todo: is this needed? Do we need write capabilities? If not, just use Wagtail's api to
    list the items.
    """
    serializer_class = ItemSerializer
    queryset = ItemDetailPage.objects.all()

class ItemDetailListView(RetrieveUpdateDestroyAPIView):
    """
    Gets a specific item with GET, PUT, POST, and DELETE request capabilities.
    """
    serializer_class = ItemSerializer
    queryset = ItemDetailPage.objects.all()


"""Cart & Order API Views"""
class CartOrderCreateView(CreateAPIView):
    """
    Test
    """
    serializer_class = CartSerializer
    #permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        pass


"""User API Views"""

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    """
    Needs the JWT token to be passed in order to return the serialized data.
    That is, the user needs to be logged in to access his/her profile data.
    Only logged-in, admin users can use this view.
    """
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    """
    Needs the JWT token to be passed in order to return the serialized data.
    That is, the user needs to be logged in to access his/her profile data.
    Only logged-in, admin users can use this view.
    """
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    # If the user has put in two names, separate it into first_name and last_name and save that data.
    try:
        first_name = request.data['name'].split()[0]
        last_name = request.data['name'].split()[1]

        user.first_name = first_name
        user.last_name = last_name
        user.username = request.data['email']
        user.email = request.data['email']

        # Only modify the password if the field isn't empty.
        if request.data['password'] != '':
            user.password = make_password( request.data['password'] )

        user.save()
        return Response(serializer.data)

    # For users who enter one name.
    except:
        user.first_name = request.data['name']
        user.last_name = ''
        user.username = request.data['email']
        user.email = request.data['email']

        if request.data['password'] != '':
            user.password = make_password( request.data['password'] )

        user.save()
        return Response(serializer.data)

class UserListView(ListAPIView):
    """
    Returns a list of users. Only admins can view it.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    #permission_classes = [IsAdminUser]

class UserCreateView(CreateAPIView):
    serializer_class = UserSerializerWithToken
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Adds create functionality to the User model via this API view.
        It will fill out the first_name and last_name if there are 2 names given.
        If one is given, set that name as the first name
        """
        print('password: ', request.data['password'])

        # If the user has put in two names, separate it into first_name and last_name and save that data.
        # @todo: Registering a user with 2 names works, but one name does not. Returns "user with this email already exists."???
        try:
            first_name = request.data['name'].split()[0]
            last_name = request.data['name'].split()[1]

            # Error handling when create user fails (Will show an error message rendered in the frontend).
            # Validation comes from checking username uniqueness, and will fail to create the user if,
            # a current user's username is the same.
            try:
                user_data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': request.data['email'],
                    'email': request.data['email'],
                    'password': make_password( request.data['password'] )
                }

                # Serialize the passed in user_data.
                serializer = UserSerializerWithToken(data=user_data, many=False)

                # Validate the serialized data.
                serializer.is_valid(raise_exception=True)

                # If validation is good, create the new user object.
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                #return Response(serializer.data, status=status.HTTP_201_CREATED)

            except:
                message = {'detail': 'User with this email already exists'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

        # If the user put in one name, save that name as the first name.
        except:

            # Error handling when create user fails (Will show an error message rendered in the frontend).
            # Validation comes from checking username uniqueness, and will fail to create the user if,
            # a current user's username is the same.
            try:
                user_data = {
                    'first_name': request.data['name'],
                    'last_name': '',
                    'username': request.data['email'],
                    'email': request.data['email'],
                    'password': make_password( request.data['password'] )
                }


                # Serialize the passed in user_data.
                serializer = UserSerializerWithToken(data=user_data, many=False)

                # Validate the serialized data.
                serializer.is_valid(raise_exception=True)

                # If validation is good, create the new user object.
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

            except:
                message = {'detail': 'User with this email already exists'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)




"""Simple JWT Serializer & View"""

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        """Adds non-encoded data to the token."""
        data = super().validate(attrs)

        # Get the fields from the user profile serializer.
        serializer = UserSerializerWithToken(self.user).data

        for fields, values in serializer.items():
            data[fields] = values

        print('token:', data)

        return data


class MyTokenObtainPairSerializers(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.username
        # ...

        return token



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer