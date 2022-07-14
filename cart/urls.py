from django.urls import path, include
from .views import cart_update, CartItemList, clear_cart, Checkout, on_checkout_login

app_name = 'cart'

urlpatterns = [
    path('update/', cart_update, name="update_cart"),
    path('clear/', clear_cart, name="clear_cart"),
    path('list/', CartItemList.as_view(), name="item_list"),
    path('login/', on_checkout_login, name="checkout_login"),
    path('checkout/', Checkout.as_view(), name="checkout"),
]

