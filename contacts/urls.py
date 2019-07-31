from django.urls import path
from contacts.views import contact, about

app_name = 'contacts'

urlpatterns = [
    path('', contact, name='contact'),
    path('about/', about, name='about'),

]