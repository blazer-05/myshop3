from django.urls import path
from profiles.views import user_profile, user_profile_edit

urlpatterns = [
    path('', user_profile, name='user_profile'),
    path('edit/', user_profile_edit, name='user_profile_edit'),


]
