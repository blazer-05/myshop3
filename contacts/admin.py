from django.contrib import admin
from contacts.models import Contacts, Maps, About
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    pass


@admin.register(Maps)
class MapsAdmin(admin.ModelAdmin):
    pass


@admin.register(About)
class AboutAdmin(SummernoteModelAdmin):
    pass