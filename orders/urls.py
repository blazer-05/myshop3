from django.urls import path
from django.views.generic import TemplateView

from orders.views import order_create

app_name = 'orders'

urlpatterns = [
    path('create/', order_create, name='create_orders'),
    path('create/thanks/', TemplateView.as_view(template_name='orders/thanks.html'), name='thanks'),


]