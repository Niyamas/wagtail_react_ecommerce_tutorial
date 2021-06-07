from django.urls import path
from api.views import (
    getRoutes,

    ItemListView,
    ItemDetailListView,

    getUserProfile,
    UserListView,
    UserCreateView,

    MyTokenObtainPairSerializer,
    MyTokenObtainPairView
)

from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('', getRoutes, name='routes'),

    path('users/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),     # DRF simple JWT: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html
    
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/profile/', getUserProfile, name='user-profile'),
    path('users/register/', UserCreateView.as_view(), name='user-register'),

    path('items/', ItemListView.as_view(), name='item-list'),
    path('item/<int:pk>/', ItemDetailListView.as_view(), name='item-detail')
]