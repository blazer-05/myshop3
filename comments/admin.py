from django.contrib import admin
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin

from comments.models import Comment

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


@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    list_display = ['id', 'content_object', 'sender', 'is_authenticated', 'text_format', 'email', 'like', 'dislike', 'is_active', 'created', 'updated']
    list_editable = ['is_active', ]
    list_display_links = ['content_object']  # Выводит в админке какие поля будут в виде ссылок.
    list_per_page = 10  # Вывод количества комментариев в админке
    actions = [complete_post, incomplete_post]  # Методы complete_post, incomplete_post для массового снятия/публикации товаров.

    def sender(self, obj):
        '''Метод определяет в одном столбце кто добавил комментарий user или user_name (т.е. зарегистрированный или нет пользовватель)'''
        return obj.user or obj.user_name

    sender.short_description = 'Отправитель'

    def is_authenticated(self, obj):
        '''Метод определяет в одном столбце от кого был комментарий от авторизаванного или анонимного пользователя'''
        return bool(obj.user)

    is_authenticated.short_description = 'Зарегистрирован'
    is_authenticated.boolean = True

    def text_format(self, obj):
        '''Метод, который убирает в админке в поле text теги <p><br></p> от визуального редактора Summernote. В настройках суммернота не получилось это сделать.'''
        return mark_safe(obj.text)

    text_format.short_description = 'Комментарии'

    def content_object(self, content_object):
        return content_object

    content_object.short_description = 'Новость'



