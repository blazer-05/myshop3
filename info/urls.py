from django.urls import path
from info.views import newslist, newsdetails

app_name = 'info'

urlpatterns = [

    path('list/', newslist, name='newslist'),
    # path('mail/', admin_comment_email, name='mail'),
    path('details/<slug>/', newsdetails, name='newsdetails'),

    # path('like/', like, name='like'),
    # path('dislike/', dislike, name='dislike'),
    # #path('success/', success, name='success'),
    #
    # path('comment/<int:pk>/edit-comment/', edit_comment, name='edit_comment'),
    # path('comment/<int:pk>/delete-comment/', delete_comment, name='delete_comment'),



]

