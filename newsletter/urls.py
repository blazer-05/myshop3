from django.urls import path
from .views import newsletter_unsubscribe

urlpatterns = [

    path('unsubscribe/', newsletter_unsubscribe, name='newsletter_unsubscribe'),


]