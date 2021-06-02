from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView
)

from .products import products



@api_view(['GET'])
def getRoutes(request):
    """API v1 home page."""

    routes = {
        'Product list': '/api/v1/products/',
    }

    return Response(routes)

@api_view(['GET'])
def getProducts(request):
    return Response(products)

@api_view(['GET'])
def getProduct(request, pk):

    product = None

    for i in products:
        if i['_id'] == pk:
            product = i
            break
        
    return Response(product)