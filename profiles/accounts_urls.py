from django.conf.urls import url
from profiles.views import password_change

# Урл для смены пароля в профиле пользователя
urlpatterns = [
    url(r"^password/change/$", password_change,
        name="account_change_password"),
]

