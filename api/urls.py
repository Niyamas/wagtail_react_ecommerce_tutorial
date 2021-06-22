from django.urls import path
from api.views import (
    getRoutes,

    ItemListView,
    ItemDetailListView,
    ItemListTopItemsView,

    getUserProfile,
    updateUserProfile,
    UserListView,
    UserCreateView,
    MyTokenObtainPairView,
    ReviewCreateView,

    CartOrderCreateView,
    CartDetailView,
    CartUpdatePaidView,
    CartCustomerListView
)

#from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('', getRoutes, name='routes'),

    # User
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),     # DRF simple JWT: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html
    path('users/profile/', getUserProfile, name='user-profile'),
    path('users/profile/update/', updateUserProfile, name='user-profile-update'),
    path('users/register/', UserCreateView.as_view(), name='user-register'),

    # Item
    path('items/', ItemListView.as_view(), name='item-list'),
    path('items/top/', ItemListTopItemsView.as_view(), name='item-list-top'),
    path('item/<int:pk>/', ItemDetailListView.as_view(), name='item-detail'),
    path('item/<str:pk>/reviews/', ReviewCreateView.as_view(), name='review-add'),

    # Cart
    path('cart/add/', CartOrderCreateView.as_view(), name='cart-order-add'),
    path('cart/<str:pk>/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/<str:pk>/pay/', CartUpdatePaidView.as_view(), name='cart-pay'),
    path('my-orders/', CartCustomerListView.as_view(), name='my-orders'),
]