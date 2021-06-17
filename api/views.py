from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.forms.models import model_to_dict
from django.utils import timezone

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
    RetrieveAPIView,
    UpdateAPIView
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
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        
        # Store the request data that is passed to this view.
        user = request.user
        data = request.data

        #print('user:', user, 'type:', type(user), 'user.first_name:', user.first_name)

        # Orders data passed from the frontend via request to this view.
        orders = data['orders']

        # Check if there are orders in the customer's cart.
        if orders and len(orders) == 0:

            # If there are no orders in the cart, send a message to the frontend called 'detail'.
            return Response({'detail': 'No order items'}, status=status.HTTP_400_BAD_REQUEST)

        else:

            ### (1) Create cart. Boolean values will be updated later.
            # Create new Cart object from the data given from the frontend.
            """ cart = Cart.objects.create(
                user=user,
                payment_method=data['payment_method'],
                shipping_price=data['shipping_price'],
                tax_price=data['tax_price'],
                total_price=data['total_price']
            ) """

            cart_data = {
                'user': user.id,
                'payment_method': data['payment_method'],
                'shipping_price': data['shipping_price'],
                'tax_price': data['tax_price'],
                'total_price': data['total_price']
            }

            #print('cart data = ', cart.user)

            serializer = CartSerializer(data=cart_data, many=False)
            serializer.is_valid(raise_exception=True)
            cart_serialized_obj = serializer.save()

            print('serialized cart data = ', cart_serialized_obj)

            #self.perform_create(serializer)


            ### (2) Create shipping address
            # Create new ShippingAddress object from the frontend data.
            shipping_address = ShippingAddress.objects.create(
                cart=cart_serialized_obj,
                address=data['shipping_address']['address'],
                city=data['shipping_address']['city'],
                postal_code=data['shipping_address']['postalCode'],
                country=data['shipping_address']['country']
            )

            # (3) Create orders and assign each order to the new cart.
            for order in orders:
                item = ItemDetailPage.objects.all().get(id=order['id'])

                order = Order.objects.create(
                    item=item,
                    image=item.image.file.url,
                    cart=cart_serialized_obj,
                    name=item.title,
                    quantity=order['quantity'],
                    price=order['price']
                )

                ### (4) Update stock. Objects can use dot notation!
                item.quantity_in_stock -= order.quantity
                item.save()

            """ serializer = CartSerializer(data=model_to_dict(cart), many=False)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            print('serializer = ', serializer)
            print('serializer data = ', serializer.data) """
            return Response(serializer.data)

class CartDetailView(RetrieveAPIView):
    """"""
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        cart = self.get_object()

        #return self.retrieve(request, *args, **kwargs)

        try:
            if user.is_staff or cart.user == user:
                return self.retrieve(request, *args, **kwargs)
            else:
                Response({'detail': 'Not authorized to view this order.'}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'detail': 'Order does not exits'}, status=status.HTTP_400_BAD_REQUEST)




class CartUpdatePaidView(UpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    #permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_paid = True
        instance.paid_at = timezone.now()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)






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

        #print('token:', data)

        return data






class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer