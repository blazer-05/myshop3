from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin

from .models import Banners, News
#from .views import newsdetails


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

    # def comments_count(self, obj):
    #     '''Для вывода колонки количества комментариев к статье в админке'''
    #     return obj.comments_count
    # comments_count.short_description = 'Кол-во комментариев'
    # comments_count.admin_order_field = 'comments_count'
    #
    # def get_queryset(self, request):
    #     '''Для вывода колонки количества комментариев к статье в админке'''
    #     return super().get_queryset(request).with_comments_count()


'''
@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    list_display = ['id', 'content_object', 'sender', 'is_authenticated', 'text_format', 'email', 'like', 'dislike', 'is_active', 'created', 'updated']
    list_editable = ['is_active', ]
    list_display_links = ['content_object']  # Выводит в админке какие поля будут в виде ссылок.
    list_per_page = 10  # Вывод количества комментариев в админке
    actions = [complete_post, incomplete_post]  # Методы complete_post, incomplete_post для массового снятия/публикации товаров.

    def sender(self, obj):
        Метод определяет в одном столбце кто добавил комментарий user или user_name (т.е. зарегистрированный или нет пользовватель)
        return obj.user or obj.user_name

    sender.short_description = 'Отправитель'

    def is_authenticated(self, obj):
        Метод определяет в одном столбце от кого был комментарий от авторизаванного или анонимного пользователя
        return bool(obj.user)

    is_authenticated.short_description = 'Зарегистрирован'
    is_authenticated.boolean = True

    def text_format(self, obj):
        Метод, который убирает в админке в поле text теги <p><br></p> от визуального редактора Summernote. В настройках суммернота не получилось это сделать.
        return mark_safe(obj.text)

    text_format.short_description = 'Комментарии'

    def content_object(self, content_object):
        return content_object

    content_object.short_description = 'Новость'


'''