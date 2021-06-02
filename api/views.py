from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView
)

from api.serializers import (
    ReviewSerializer,
    ItemSerializer
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


@api_view(['GET'])
def getRoutes(request):
    """
    API v1 home page.
    """
    routes = {
        'Item list': '/api/v1/items/',
        'Item details': '/api/v1/item/<int:pk>/'
    }

    return Response(routes)

@api_view(['GET'])
def getProducts(request):
    products = ItemDetailPage.objects.all()
    return Response(products)



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