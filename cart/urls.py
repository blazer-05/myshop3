from django.urls import path
from cart.views import (CartTemplateView, CartInfoTemplateView, CartAddFormView,
                        CartChangeFormView, CartRemoveFormView, CheckoutTemplateView)


app_name = 'cart'

urlpatterns = [
    path('', CartTemplateView.as_view(), name='cart'),
    path('info/', CartInfoTemplateView.as_view(), name='info'),
    path('add/', CartAddFormView.as_view(), name='add'),
    path('change/', CartChangeFormView.as_view(), name='change'),
    path('remove/', CartRemoveFormView.as_view(), name='remove'),
    path('checkout/', CheckoutTemplateView.as_view(), name='checkout'),
]