from django.urls import path
from info.views import newslist, newsdetails, create_review


app_name = 'info'

urlpatterns = [

    path('list/', newslist, name='newslist'),
    path('details/<slug>/', newsdetails, name='newsdetails'),

    path('create-review/', create_review, name='create-review'),
]

