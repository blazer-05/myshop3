from django.urls import path
from info.views import newslist, newsdetails, admin_comment_email, like, dislike

app_name = 'info'

urlpatterns = [

    path('list/', newslist, name='newslist'),
    path('mail/', admin_comment_email, name='mail'),
    path('details/<slug>/', newsdetails, name='newsdetails'),
    path('like/', like, name='like'),
    path('dislike/', dislike, name='dislike'),



]