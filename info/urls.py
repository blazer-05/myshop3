from django.urls import path

from info.templatetags.review import review_list
from info.views import newslist, newsdetails


app_name = 'info'

urlpatterns = [

    path('list/', newslist, name='newslist'),
    path('details/<slug>/', newsdetails, name='newsdetails'),

    path('create-review/', review_list, name='create-review'),
]

