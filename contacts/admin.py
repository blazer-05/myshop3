from django.contrib import admin
from contacts.models import Contacts, Maps, About, Address, PrivacyPolicy, Backcall
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


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(SummernoteModelAdmin):
    pass


@admin.register(Backcall)
class BackcallAdmin(admin.ModelAdmin):
    pass