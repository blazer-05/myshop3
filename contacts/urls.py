from django.urls import path
from contacts.views import contact, about, backcall, delivery

app_name = 'contacts'

urlpatterns = [
    path('', contact, name='contact'),
    path('about/', about, name='about'),
    path('backcall/', backcall, name='backcall'),
    path('delivery/', delivery, name='delivery'),

]