from django.urls import path
from info.views import newslist, newsdetails
from info.templatetags.review import review_list

app_name = 'info'

urlpatterns = [

    path('list/', newslist, name='newslist'),
    path('details/<slug>/', newsdetails, name='newsdetails'),

    path('review-list/', review_list, name='review_list'),
]

