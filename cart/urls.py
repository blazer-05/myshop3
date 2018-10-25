from django.urls import path
from cart.views import checkout, CartViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', CartViewSet)

app_name = 'cart'

urlpatterns = [

    path('checkout/', checkout, name='checkout'),

] + router.urls