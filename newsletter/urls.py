from django.urls import path
from .views import (
    newsletter_unsubscribe,
    subscribe, control_newsletter,
    control_newsletter_list,
    control_newsletter_detail,
    control_newsletter_edit,
    control_newsletter_delete,
    )

urlpatterns = [
    path('subscribe/', subscribe, name='subscribe'),
    path('unsubscribe/', newsletter_unsubscribe, name='newsletter_unsubscribe'),
    path('dashboard/', control_newsletter, name='control_newsletter'),
    path('dashboard/list/', control_newsletter_list, name='control_newsletter_list'),
    path('dashboard/detail/<int:pk>/', control_newsletter_detail, name='control_newsletter_detail'),
    path('dashboard/edit/<int:pk>/', control_newsletter_edit, name='control_newsletter_edit'),
    path('dashboard/delete/<int:pk>/', control_newsletter_delete, name='control_newsletter_delete'),

]