from django.urls import path
from contacts.views import contact, about, backcall

app_name = 'contacts'

urlpatterns = [
    path('', contact, name='contact'),
    path('about/', about, name='about'),
    path('backcall/', backcall, name='backcall'),

]