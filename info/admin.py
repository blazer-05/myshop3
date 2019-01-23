from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Banners, News, Comments

# Функции фильтрации для массовой публикации/снятия с публикации новостей.
def all_post(modeladmin, request, queryset):
    for qs in queryset:
        print(qs.title)

def complete_post(modeladmin, request, queryset):
    queryset.update(is_active=True)
complete_post.short_description = 'Опубликовать новость'

def incomplete_post(modeladmin, request, queryset):
    queryset.update(is_active=False)
incomplete_post.short_description = 'Снять с публикации новость'
# Конец Функции фильтрации

class BannersAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'image_img', 'link', 'is_active', 'created', 'updated']
    list_editable = ['is_active']
    list_display_links = ['title']
    actions = [complete_post, incomplete_post]  # Методы complete_post, incomplete_post для массового снятия/публикации товаров.

admin.site.register(Banners, BannersAdmin)

@admin.register(News)
class NewsAdmin(SummernoteModelAdmin):
    list_display = ['id', 'title', 'slug', 'image_img', 'count', 'is_active', 'user', 'created', 'updated']
    list_editable = ['is_active']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['image_img']  # Выводит в карточке товара картинку товара!
    list_display_links = ['title']   # Выводит в админке какие поля будут в виде ссылок.
    search_fields = ['id', 'title', 'slug']  # Выводит строку поиска в адинке
    list_filter = ['id', 'title', 'user', 'is_active', 'created', 'updated']
    actions = [complete_post, incomplete_post]  # Методы complete_post, incomplete_post для массового снятия/публикации товаров.
    list_per_page = 10  # Вывод количества новостей в админке

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'news', 'user', 'text', 'email', 'like', 'dislike', 'count', 'is_active', 'created', 'updated']
    list_editable = ['is_active', ]
    list_display_links = ['news']  # Выводит в админке какие поля будут в виде ссылок.


