from django.urls import path

from info.templatetags.review import review_list
from info.views import newslist, newsdetails, create_review, edit_review


app_name = 'info'

urlpatterns = [

    path('list/', newslist, name='newslist'),
    path('details/<slug>/', newsdetails, name='newsdetails'),

    path('create-review/', create_review, name='create-review'),
    path('review/<int:pk>/edit-review/', edit_review, name='edit_review'),
    #path('review/<int:pk>/delete-review/', delete_review, name='delete_review'),
]

