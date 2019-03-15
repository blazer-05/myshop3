from django.urls import path
from comments.templatetags.comments import like, dislike, edit_comment, delete_comment

app_name = 'comments'

urlpatterns = [

    path('like/', like, name='like'),
    path('dislike/', dislike, name='dislike'),
    #path('success/', success, name='success'),

    path('comment/<int:pk>/edit-comment/', edit_comment, name='edit_comment'),
    path('comment/<int:pk>/delete-comment/', delete_comment, name='delete_comment'),



]