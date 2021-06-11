from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.forms.models import model_to_dict

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    CreateAPIView,
)

from api.serializers import (
    ReviewSerializer,
    ItemSerializer,

    UserSerializer,
    UserSerializerWithToken,

    CartSerializer,
    OrderSerializer,
    ShippingAddressSerializer
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


"""Item API Views"""

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




"""Cart API Views"""

#@permission_classes(['IsAuthenticated'])
class CartOrderCreateViewBRICK(CreateAPIView):
    """
    """
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        return serializer.save()
    
    def create(self, request, *args, **kwargs):

        # Store the request data that is passed to this view.
        user = request.user
        data = request.data

        print('user',user)

        # Orders data passed from the frontend via request to this view.
        orders = data['orders']

        # Check if there are orders in the customer's cart.
        if orders and len(orders) == 0:

            # If there are no orders in the cart, send a message to the frontend called 'detail'.
            return Response({'detail': 'No order items'}, status=status.HTTP_400_BAD_REQUEST)

        else:

            # (1) Create cart. Boolean values will be updated later.
            cart_data = {
                'user': user,
                'payment_method': data['payment_method'],
                'tax_price': data['tax_price'],
                'shipping_price': data['shipping_price'],
                'total_price': data['total_price'],
            }

            # Validate, serialize, and save the data.
            cart_serializer = CartSerializer(data=cart_data, many=False)
            cart_serializer.is_valid(raise_exception=True)
            newly_created_cart = cart_serializer.save()
            #headers = self.get_success_headers(cart_serializer)

            print('newly_created_cart', newly_created_cart)

            # (2) Create shipping address
            shipping_address_data = {
                'cart': model_to_dict(newly_created_cart, fields=['user', 'payment_method', 'tax_price', 'shipping_price', 'total_price']),
                'address': data['shipping_address']['address'],
                'city': data['shipping_address']['city'],
                'postal_code': data['shipping_address']['postalCode'],
                'country': data['shipping_address']['country'],
            }

            # Validate, serialize, and save the data.
            shipping_address_serializer = ShippingAddressSerializer(data=shipping_address_data, many=False)
            shipping_address_serializer.is_valid(raise_exception=True)
            self.perform_create(shipping_address_serializer)
            #headers = self.get_success_headers(shipping_address_serializer)

            # (3) Create orders and assign each order to the new cart.
            for order in orders:
                item = ItemDetailPage.objects.all().get(id=order['id'])

                order_data = {
                    'item': item,
                    'image': item.image.file.url,   # @ todo, see if this serializes correctly the URL.
                    'cart': newly_created_cart,
                    'name': item.title,
                    'quantity': order['quantity'],
                    'price': order['price'],
                }

                # Validate, serialize, and save the data.
                order_serializer = OrderSerializer(data=order_data, many=False)
                order_serializer.is_valid(raise_exception=True)
                newly_created_order = order_serializer.save()
                #headers = self.get_success_headers(order_serializer)

            # (4) Update stock. Objects can use dot notation!
            item.quantity_in_stock -= newly_created_order.quantity
            item.save()

            # Return the serialized cart data to the frontend or API page.
            cart_serializer.is_valid(raise_exception=True)
            return Response(cart_serializer.data)


#@permission_classes(['IsAuthenticated'])
class CartOrderCreateView(CreateAPIView):
    """
    Test
    """
    serializer_class = CartSerializer
    
    def create(self, request, *args, **kwargs):

        # Store the request data that is passed to this view.
        user = request.user
        data = request.data

        # Orders data passed from the frontend via request to this view.
        orders = data['orders']

        # Check if there are orders in the customer's cart.
        if orders and len(orders) == 0:

            # If there are no orders in the cart, send a message to the frontend called 'detail'.
            return Response({'detail': 'No order items'}, status=status.HTTP_400_BAD_REQUEST)

        else:

            ### (1) Create cart. Boolean values will be updated later.
            # Create new Cart object from the data given from the frontend.
            cart = Cart.objects.create(
                user=user,
                payment_method=data['payment_method'],
                shipping_price=data['shipping_price'],
                tax_price=data['tax_price'],
                total_price=data['total_price']
            )

            print('cart:', cart, 'type:', type(cart))

            ### (2) Create shipping address
            # Create new ShippingAddress object from the frontend data.
            shipping_address = ShippingAddress.objects.create(
                cart=cart,
                address=data['shipping_address']['address'],
                city=data['shipping_address']['city'],
                postal_code=data['shipping_address']['postalCode'],
                country=data['shipping_address']['country']
            )

            # (3) Create orders and assign each order to the new cart.
            for order in orders:
                item = ItemDetailPage.objects.all().get(id=order['id'])

                order_data = {
                    'item': item,
                    'image': item.image.file.url,   # @ todo, see if this serializes correctly the URL.
                    'cart': cart,
                    'name': item.title,
                    'quantity': order['quantity'],
                    'price': order['price'],
                }

                order = Order.objects.create(
                    item=item,
                    image=item.image.file.url,
                    cart=cart,
                    name=item.title,
                    quantity=order['quantity'],
                    price=order['price']
                )

                ### (4) Update stock. Objects can use dot notation!
                item.quantity_in_stock -= order.quantity
                item.save()

                print('cart fields:', cart._meta.fields)

            # Return the serialized cart data to the frontend or API page.
            serializer = CartSerializer(data=cart, many=False)
            serializer.is_valid()
            return Response(serializer.data)


@api_view(['POST'])
#@permission_classes(['IsAuthenticated'])
def createCartAddOrders(request):
    """"""
    # Store the request data that is passed to this view.
    user = request.user
    data = request.data

    # Orders data passed from the frontend via request to this view.
    orders = data['orders']

    # Check if there are orders in the customer's cart.
    if orders and len(orders) == 0:

        # If there are no orders in the cart, send a message to the frontend called 'detail'.
        return Response({'detail': 'No order items'}, status=status.HTTP_400_BAD_REQUEST)

    else:

        ### (1) Create cart. Boolean values will be updated later.
        # Create new Cart object from the data given from the frontend.
        cart = Cart.objects.create(
            user=user,
            payment_method=data['payment_method'],
            shipping_price=data['shipping_price'],
            tax_price=data['tax_price'],
            total_price=data['total_price']
        )

        #print('cart:', cart, 'type:', type(cart))

        ### (2) Create shipping address
        # Create new ShippingAddress object from the frontend data.
        shipping_address = ShippingAddress.objects.create(
            cart=cart,
            address=data['shipping_address']['address'],
            city=data['shipping_address']['city'],
            postal_code=data['shipping_address']['postalCode'],
            country=data['shipping_address']['country']
        )

        # (3) Create orders and assign each order to the new cart.
        for order in orders:
            item = ItemDetailPage.objects.all().get(id=order['id'])

            order_data = {
                'item': item,
                'image': item.image.file.url,   # @ todo, see if this serializes correctly the URL.
                'cart': cart,
                'name': item.title,
                'quantity': order['quantity'],
                'price': order['price'],
            }

            order = Order.objects.create(
                item=item,
                image=item.image.file.url,
                cart=cart,
                name=item.title,
                quantity=order['quantity'],
                price=order['price']
            )

            ### (4) Update stock. Objects can use dot notation!
            item.quantity_in_stock -= order.quantity
            item.save()

        # Return the serialized cart data to the frontend or API page.
        #serializer = CartSerializer(data=cart, many=False)
        #serializer.is_valid(raise_exception=True)
        #return Response(serializer.data)
        return Response('Brown')




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




#@permission_classes([IsAdminUser])
class UserListView(ListAPIView):
    """
    Returns a list of users. Only admins can view it.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserCreateView(CreateAPIView):
    serializer_class = UserSerializerWithToken
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Adds create functionality to the User model via this API view.
        It will fill out the first_name and last_name if there are 2 names given.
        If one is given, set that name as the first name
        """

        # If the user has put in two names, separate it into first_name and last_name and save that data.
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
                serializer = self.get_serializer(data=user_data, many=False)

                # Validate the serialized data.
                serializer.is_valid(raise_exception=True)

                # If validation is good, create the new user object.
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

            except:
                message = {'detail': 'User with this email already exists'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)



# {"name":"Galuf","email":"galuf@email.com","password":"Ddfquuwhewr9"}



"""Simple JWT serializers"""

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        """Adds non-encoded data to the token."""
        data = super().validate(attrs)

        # Get the fields from the user profile serializer.
        serializer = UserSerializerWithToken(self.user).data

        #data['username'] = self.user.username
        #data['email'] = self.user.email
        #data['first_name'] = self.user.first_name
        #data['last_name'] = self.user.last_name
        #data['is_admin'] = self.user.is_admin

        for fields, values in serializer.items():
            data[fields] = values

        print('data:', data)

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



#"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI0MzkzMjMwLCJqdGkiOiJhODI0NjVjZWZkNWY0N2Y0ODAwMWNmMWVkZDhlNWU0OCIsInVzZXJfaWQiOjQ5fQ.os44UYI0kNwbwRegRkwT0YdJhHPZWCDunkkyR5oP05k"