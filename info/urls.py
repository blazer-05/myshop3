from django.urls import path
from info.views import newslist, newsdetails, admin_comment_email

app_name = 'info'

urlpatterns = [

    path('list/', newslist, name='newslist'),
    path('mail/', admin_comment_email, name='mail'),
    path('details/<slug>/', newsdetails, name='newsdetails'),


]