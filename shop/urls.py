from django.urls import path
from .views import (index, catalog, catlist, catlinks,
                    shoplist, productdetails,
                    modalproduct, compareproducts,
                    products_by_brand, search,
                    notify_create,
                    price_list_count,



                    )


app_name = 'shop'

urlpatterns = [
    path('', index, name='index_page'),
    path('category/<int:pk>/sort/brand/', products_by_brand, name='products-all'),
    path('category/<int:pk>/sort/brand/<slug>/', products_by_brand, name='products-by-brand'),
    path('catalog/', catalog, name='catalog'),
    path('catalog/catlist/<slug>/', catlist, name='catlist'),
    path('catlinks/<slug>/', catlinks, name='catlinks'),
    #path('shop/', shop, name='shop'),
    path('shop-list/<slug>/', shoplist, name='shop-list'),
    path('product-details/<str:product_slug>/', productdetails, name='product-details'),
    path('modal-product/<slug>/', modalproduct, name='modal-product'),
    path('compare-products/<category_slug>/', compareproducts, name='compare-products-by-category'),
    path('compare-products/', compareproducts, name='compare-products'),
    path('search/', search, name='search'),
    path('notify_create/', notify_create, name='notify_create'),
    path('price/<pk>/', price_list_count, name='price_list_count'),




]