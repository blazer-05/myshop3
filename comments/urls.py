from django.urls import path
from comments.views import like, dislike, edit_comment, delete_comment, create_comment

app_name = 'comments'

urlpatterns = [

    path('like/', like, name='like'),
    path('dislike/', dislike, name='dislike'),
    path('create-comment/', create_comment, name='create_comment'),

    path('comment/<int:pk>/edit-comment/', edit_comment, name='edit_comment'),
    path('comment/<int:pk>/delete-comment/', delete_comment, name='delete_comment'),



]