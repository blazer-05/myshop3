from django.urls import path
from info.views import (newslist,
                        newsdetails,
                        create_review,
                        edit_review,
                        delete_review,
                        like_review,
                        dislike_review)


app_name = 'info'

urlpatterns = [

    path('list/', newslist, name='newslist'),
    path('details/<slug>/', newsdetails, name='newsdetails'),

    path('create-review/', create_review, name='create-review'),
    path('review/<int:pk>/edit-review/', edit_review, name='edit_review'),
    path('review/<int:pk>/delete-review/', delete_review, name='delete_review'),

    path('like-review/', like_review, name='like_review'),
    path('dislike-review/', dislike_review, name='dislike_review'),

]

