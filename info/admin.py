from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.db.models import OuterRef, Count, Subquery, IntegerField
from django.db.models.functions import Coalesce

from django_summernote.admin import SummernoteModelAdmin

from comments.models import Comment
from .models import Banners, News, Review


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


class BannersAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'image_img', 'link', 'is_active', 'created', 'updated']
    list_editable = ['is_active']
    list_display_links = ['title']
    actions = [complete_post, incomplete_post]  # Методы complete_post, incomplete_post для массового снятия/публикации товаров.


admin.site.register(Banners, BannersAdmin)


@admin.register(News)
class NewsAdmin(SummernoteModelAdmin):
    list_display = ['id', 'title', 'slug', 'image_img', 'count', 'comments_count', 'is_active', 'user', 'created', 'updated']
    list_editable = ['is_active']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['image_img']  # Выводит в карточке товара картинку товара!
    list_display_links = ['title']   # Выводит в админке какие поля будут в виде ссылок.
    search_fields = ['id', 'title', 'slug']  # Выводит строку поиска в адинке
    list_filter = ['id', 'title', 'user', 'is_active', 'created', 'updated']
    actions = [complete_post, incomplete_post]  # Методы complete_post, incomplete_post для массового снятия/публикации товаров.
    list_per_page = 10  # Вывод количества новостей в админке

    def comments_count(self, obj):
        '''Для вывода колонки количества комментариев к статье в админке'''
        return obj.comments_count

    comments_count.short_description = 'Кол-во комментариев'
    comments_count.admin_order_field = 'comments_count'

    def get_queryset(self, request):
        '''Для вывода колонки количества комментариев к статье в админке'''
        comments = Comment.objects.filter(
            content_type=ContentType.objects.get_for_model(News),
            object_id=OuterRef('id')
        ).values(
            'content_type', 'object_id'
        ).annotate(
            count=Count('pk')
        ).order_by(
            'content_type', 'object_id'
        ).values('count')[:1]

        return super().get_queryset(request).annotate(
            comments_count=Coalesce(Subquery(comments), 0, output_field=IntegerField())
        )


@admin.register(Review)
class ReviewAdmin(SummernoteModelAdmin):
    pass