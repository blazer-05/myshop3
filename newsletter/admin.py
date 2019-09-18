from django.contrib import admin

from .models import NewsletterUser, Newsletter, Template


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


@admin.register(NewsletterUser)
class NewsletterUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'created']
    list_editable = ['is_active']
    search_fields = ['id', 'email', 'name']
    list_filter = ['name', 'email', 'created']
    list_per_page = 15
    actions = [complete_post, incomplete_post]


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['subject', 'status', 'created', 'updated']
    search_fields = ['id', 'subject']
    list_filter = ['subject', 'status', 'created', 'updated']
    filter_horizontal = ('users_email',)
    date_hierarchy = 'created'
    list_per_page = 15


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created', 'updated']
    list_editable = ['is_active']
    filter_horizontal = ('products',)
    actions = [complete_post, incomplete_post]

