from django.urls import path, re_path
from .views import *
from shop.context_processors import menucategory

app_name = 'shop'

urlpatterns = [
    path('', index, name='index_page'),
    path('catalog/', catalog, name='catalog'),
    path('catalog/catlist/<slug>', catlist, name='catlist'),
    path('catlinks/<slug>', catlinks, name='catlinks'),
    path('shop/', shop, name='shop'),
    path('shop-list/<slug>', shoplist, name='shop-list'),
    path('product-details/<albom_id>/<product_slug>', productdetails, name='product-details'),
    #re_path(r'^product-details/(?P<albom_id>\d+)/(?P<product_slug>[-\w]+)/$', productdetails, name='product-details'),
    path('wishlist/', wishlist, name='wishlist'),
    path('my-account/', myaccount, name='my-account'),
    path('contact/', contact, name='contact'),
    path('checkout/', checkout, name='checkout'),
    path('cart/', cart, name='cart'),
    path('registration/', registration, name='registration'),
    path('about/', about, name='about'),

]