from django.urls import path
from info.views import newslist, newsdetails, like, dislike, edit_comment, delete_comment

app_name = 'info'

urlpatterns = [

    path('list/', newslist, name='newslist'),
    # path('mail/', admin_comment_email, name='mail'),
    path('details/<slug>/', newsdetails, name='newsdetails'),
    path('like/', like, name='like'),
    path('dislike/', dislike, name='dislike'),
    #path('success/', success, name='success'),

    path('edit-comment/<int:pk>', edit_comment, name='edit_comment'),
    path('delete-comment/<int:pk>', delete_comment, name='delete_comment'),



]