from django.urls import path
from .views import (index, catalog, catlist, catlinks,
                    shop, shoplist, productdetails, wishlist,
                    myaccount, contact, registration, about, modalproduct,
                    compareproducts, products_by_brand
                    )


app_name = 'shop'

urlpatterns = [
    path('', index, name='index_page'),
    path('category/<int:pk>/sort/brand/', products_by_brand, name='products-all'),
    path('category/<int:pk>/sort/brand/<slug>/', products_by_brand, name='products-by-brand'),
    path('catalog/', catalog, name='catalog'),
    path('catalog/catlist/<slug>', catlist, name='catlist'),
    path('catlinks/<slug>', catlinks, name='catlinks'),
    path('shop/', shop, name='shop'),
    path('shop-list/<slug>', shoplist, name='shop-list'),
    path('product-details/<product_slug>', productdetails, name='product-details'),
    path('wishlist/', wishlist, name='wishlist'),
    path('my-account/', myaccount, name='my-account'),
    path('contact/', contact, name='contact'),
    path('registration/', registration, name='registration'),
    path('about/', about, name='about'),
    path('modal-product/<slug>/', modalproduct, name='modal-product'),
    path('compare-products/', compareproducts, name='compare-products'),

]