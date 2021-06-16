"""Item API Views"""

from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from api.serializers.item_serializers import ItemSerializer
from items.models import ItemDetailPage


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