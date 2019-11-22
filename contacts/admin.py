from django.contrib import admin
from contacts.models import Contacts, Maps, About, Address, PrivacyPolicy, Backcall, Delivery, HeaderWidgetInfo
from django_summernote.admin import SummernoteModelAdmin


# Функции фильтрации для массовой публикации/снятия с публикации новостей.
def all_post(modeladmin, request, queryset):
    for qs in queryset:
        print(qs.title)


def complete_post(modeladmin, request, queryset):
    queryset.update(is_active=True)


complete_post.short_description = 'Опубликовать'


def incomplete_post(modeladmin, request, queryset):
    queryset.update(is_active=False)


incomplete_post.short_description = 'Снять с публикации'
# Конец Функции фильтрации


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'email', 'created']


@admin.register(Maps)
class MapsAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created', 'update']
    list_editable = ['is_active']
    actions = [complete_post, incomplete_post]


@admin.register(About)
class AboutAdmin(SummernoteModelAdmin):
    list_display = ['title', 'is_active', 'created', 'update']
    list_editable = ['is_active']
    actions = [complete_post, incomplete_post]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['title', 'email_one', 'email_two', 'website',
                    'phone_one', 'phone_two', 'address', 'is_active', 'created', 'update']
    list_editable = ['is_active']
    actions = [complete_post, incomplete_post]


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(SummernoteModelAdmin):
    list_display = ['title', 'is_active', 'created', 'update']
    list_editable = ['is_active']
    actions = [complete_post, incomplete_post]


@admin.register(Backcall)
class BackcallAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'text', 'created']


@admin.register(Delivery)
class DeliveryAdmin(SummernoteModelAdmin):
    list_display = ['title', 'is_active', 'created', 'update']
    list_editable = ['is_active']
    actions = [complete_post, incomplete_post]


@admin.register(HeaderWidgetInfo)
class HeaderWidgetInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'text']
