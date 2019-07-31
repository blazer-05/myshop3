"""myshop3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls', namespace='shop')),
    path('summernote/', include('django_summernote.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('order/', include('orders.urls', namespace='order')),
    path('news/', include('info.urls', namespace='news')),
    path('reviews/', include('info.urls', namespace='reviews')),
    path('comments/', include('comments.urls', namespace='comments')),
    path('accounts/profile/', include('profiles.urls')),
    path('captcha/', include('captcha.urls')),
    path('accounts/', include('profiles.accounts_urls')),
    path('accounts/', include('allauth.urls')),

    path('contact/', include('contacts.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)