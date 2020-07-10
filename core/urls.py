from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    HomeView,
    checkout,
    ItemDetailView,
    notifications,
    add_to_cart,
    CloginPage,
    ClogoutPage,
    CregisterPage,
    remove_from_cart
)

app_name = 'core'

urlpatterns = [
    path('customer/', HomeView.as_view(), name='item-list'),
    path('checkout/', checkout, name='checkout'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('notifications/', notifications, name='notifications'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('customer_login/', CloginPage, name="Clogin"),
    path('customer_logout/', ClogoutPage, name="Clogout"),
    path('customer_register/', CregisterPage, name="Cregister"),
]
