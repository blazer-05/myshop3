from django.urls import path, re_path
from .views import *
from shop.context_processors import menucategory

app_name = 'shop'

urlpatterns = [
    path('', index, name='index_page'),
    path('catalog/', catalog, name='catalog'),
    path('catalog/catlist/<slug,id>', catlist, name='catlist'),
    path('shop/', shop, name='shop'),
    path('shop-list/', shoplist, name='shop-list'),
    path('product-details/', productdetails, name='product-details'),
    path('wishlist/', wishlist, name='wishlist'),
    path('my-account/', myaccount, name='my-account'),
    path('contact/', contact, name='contact'),
    path('checkout/', checkout, name='checkout'),
    path('cart/', cart, name='cart'),
    path('registration/', registration, name='registration'),
    path('about/', about, name='about'),
    #path('menucat/<int:category_id>/', menucategory, name='menucat'),
]