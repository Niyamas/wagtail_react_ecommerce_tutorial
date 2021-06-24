from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core import paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.query import QuerySet
from django.utils import timezone

from rest_framework import request, status
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
from wagtail.core.models import PAGE_MODEL_CLASSES

from api.serializers.user_serializers import (
    UserSerializer,
    UserSerializerWithToken
)

from api.serializers.item_serializers import (
    ReviewSerializer,
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

from rest_framework.pagination import PageNumberPagination

class ItemListView(ListAPIView):
    """
    Lists all of the items. Can get this in Wagtail API, but that is read-only.
    Add a get_queryset method to create parameters for the URL to filter the list of items.
    @todo: is this needed? Do we need write capabilities? If not, just use Wagtail's api to
    list the items.
    """
    queryset = ItemDetailPage.objects.all()
    serializer_class = ItemSerializer
    #pagination_class = PageNumberPagination

    def get_queryset(self):
        """Adds search functionality for the home page items."""

        # Get the keyword URL parameter value. Return empty string if the keyword is empty.
        # Filter the queryset based on the value of keyword and the queryset object's title.
        keyword = self.request.query_params.get('keyword', '')
        queryset = self.queryset.filter(title__icontains=keyword).order_by('-first_published_at')

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()

        return queryset

    def list(self, request, *args, **kwargs):
        """Modification of original list method. Added different pagination method."""

        queryset = self.filter_queryset(self.get_queryset())

        page = request.query_params.get('page', 1)
        paginator = Paginator(queryset, 4)

        try:
            queryset = paginator.page(page)

        except PageNotAnInteger:
            queryset = paginator.page(1)

        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        page = int(page)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'items': serializer.data, 'page': page, 'pages': paginator.num_pages})

class ItemDetailListView(RetrieveUpdateDestroyAPIView):
    """
    Gets a specific item with GET, PUT, POST, and DELETE request capabilities.
    """
    serializer_class = ItemSerializer
    queryset = ItemDetailPage.objects.all()


class ItemListTopItemsView(ListAPIView):
    """A view to get the top items for the React carousel component to display."""

    queryset = ItemDetailPage.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):

        # Query 5 items with a rating greater than or equal to 4, in descending order(5 -> 4).
        queryset = self.queryset.filter(rating__gte=4).order_by('-rating')[0:5]

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()

        return queryset

    """ def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data) """


"""Cart & Order API Views"""

class CartOrderCreateView(CreateAPIView):
    """
    When the user clicks on the place order (before payment), it will
    create a cart, order, and shipping address object for the user in
    the database.
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

            cart_data = {
                'user': user.id,
                'payment_method': data['payment_method'],
                'shipping_price': data['shipping_price'],
                'tax_price': data['tax_price'],
                'total_price': data['total_price']
            }

            #print('cart data = ', cart.user)

            # Validate the serialized data, and store the output data.
            serializer = CartSerializer(data=cart_data, many=False)
            serializer.is_valid(raise_exception=True)
            cart_serialized_obj = serializer.save()

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
                # @ todo: will this be faster if I remove the all() part of this query?
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
    """
    Retrieves cart data for the current logged-in user.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    #permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        #user = User.objects.get(id=1)  # Testing

        cart = self.get_object()

        try:
            if user.is_staff or cart.user == user:
                return self.retrieve(request, *args, **kwargs)
            else:
                Response({'detail': 'Not authorized to view this order.'}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'detail': 'Order does not exits'}, status=status.HTTP_400_BAD_REQUEST)

class CartCustomerListView(ListAPIView):
    """
    Gets a list of carts for the current logged-in customer.
    Used in the profile "My Orders" section.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        carts = user.cart_set.all()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

class CartUpdatePaidView(UpdateAPIView):
    """
    When the user pays for their order via PayPal, update
    two fields in their cart:
    1) is_paid = True
    2) paid_at = current datetime
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

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

class ReviewCreateView(CreateAPIView):
    """"""
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, pk, *args, **kwargs):
        user = request.user
        data = request.data
        item = ItemDetailPage.objects.get(id=pk)

        ### 1) Review already exists.

        # Does a user have a review already for this item?
        already_exists = item.review_set.filter(user=user).exists()

        if already_exists:
            content = {'detail': 'Product already reviewed'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        ### 2) No rating or 0.
        elif data['rating'] == 0:
            content = {'detail': 'Please select a rating'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        ### 3) Create review object.
        else:
            review_data = {
                'item': item.id,   # @ todo: use item.id
                'user': user.id,
                'name': user.first_name,
                'rating': data['rating'],
                'comment': data['comment']
            }

            # Serialize and save the new review object in the database
            serializer = ReviewSerializer(data=review_data, many=False)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            reviews = item.review_set.all()
            item.quantity_reviews = len(reviews)

            # After creating the new review object, recaclulate the item's star rating.
            total = 0
            for review in reviews:
                total += review.rating
            item.rating = total / len(reviews)
            item.save()

            return Response( {'detail': 'Review added'} )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)




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
    permission_classes = [IsAdminUser]

class UserCreateView(CreateAPIView):
    """
    A view for creating/registering users. If two names are provided,
    set those as first_name and last_name. If there's one name, save it
    as first_name and leave last_name blank.
    """
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