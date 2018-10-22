from django.urls import path
from cart.views import cart_view, add_to_cart_view, remove_from_cart_view, change_item_qty, checkout

app_name = 'cart'

urlpatterns = [

    path('', cart_view, name='cart'),
    path('add_to_cart/', add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/', remove_from_cart_view, name='remove_from_cart'),
    path('change_item_qty/', change_item_qty, name='change_item_qty'),
    path('checkout/', checkout, name='checkout'),

]