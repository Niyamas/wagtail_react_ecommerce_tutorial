from rest_framework.response import Response
from rest_framework.decorators import api_view


"""Home API View"""
@api_view(['GET'])
def getRoutes():
    """
    API v1 home page.
    """
    routes = {
        'Item list': '/api/v1/items/',
        'Item details': '/api/v1/item/<int:pk>/',

        'JWT': '/api/v1/users/login/',
    }

    return Response(routes)