from django.urls import path
from api.views import (
    getRoutes,

    ItemListView,
    ItemDetailListView
)

urlpatterns = [
    path('', getRoutes, name='routes'),

    path('items/', ItemListView.as_view(), name='item-list'),
    path('item/<int:pk>/', ItemDetailListView.as_view(), name='item-detail')
]