from django.urls import path
from info.views import newslist, newsdetails

app_name = 'info'

urlpatterns = [

    path('list/', newslist, name='newslist'),
    path('details/<slug>/', newsdetails, name='newsdetails'),

]