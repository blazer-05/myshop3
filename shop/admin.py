from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from mptt.admin import DraggableMPTTAdmin
from mptt.admin import TreeRelatedFieldListFilter

from shop.models import Category, Brand, Product, ProductAlbomImages, Attribute, Value, Entry

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'image_img', 'slug', 'description', 'is_active', 'created', 'updated']
    readonly_fields = ['image_img', ]

# Класс модели Entry для вывода атрибута и значения
class EntryInline(admin.TabularInline):
    model = Entry
    fields = ('attribute', 'value', 'is_active')
    extra = 0


# Класс модели продукта
class ProductAdmin(SummernoteModelAdmin):
    inlines = [EntryInline] # Привязываем модель EntryInline в админке к товару.
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'category', 'brand', 'slug', 'image_img', 'price', 'stock', 'is_active', 'created', 'updated']
    readonly_fields = ['image_img', ] # Выводит в карточке товара картинку товара!
    list_filter = (#'category',
                   ('category', TreeRelatedFieldListFilter),
                   'brand',
                   'is_active',
                   'created',
                   'updated'
                   )
    search_fields = ['title']
    list_editable = ['slug', 'is_active']

admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)

# Модель Фото альбома в виде категорий
admin.site.register(
    ProductAlbomImages,
    DraggableMPTTAdmin,
    list_display = (
        'tree_actions',
        'indented_title',
        'name',
        'image_img',
        'product',
        'is_active',
        'created',
        'updated'
    ),
    list_display_links=(
        'indented_title',
    ),
    list_filter=(
        # 'name',       # Вывод фильтра по категориям справа экрана
        ('parent', TreeRelatedFieldListFilter),  # Вывод фильтра по категориям справа экрана с потомками родителя
    ),
    readonly_fields = ['image_img']
)

# В модели категорий делаем внешний вид согласно инструкции
# https://django-mptt.readthedocs.io/en/latest/admin.html#mptt-admin-draggablempttadmin
admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        'image_img',
        'slug',
        'is_active',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
    list_filter=(
        #'name',       # Вывод фильтра по категориям справа экрана
        ('parent', TreeRelatedFieldListFilter), # Вывод фильтра по категориям справа экрана с потомками родителя
    ),
    list_editable = (
        'slug',
        'is_active',
    ),
    readonly_fields = ['image_img', ], # Выводит в карточке товара картинку товара!
    prepopulated_fields = {'slug': ('name',)}, # Автозаполнение поля slug
    mptt_level_indent=20 # Эта настройка задает отступ субкатегории от родительской категории
)


# Модель Аттрибута в виде категорий
admin.site.register(
    Attribute,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        'title',
        'is_active',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
    list_filter=(
        #'name',       # Вывод фильтра по категориям справа экрана
        ('parent', TreeRelatedFieldListFilter), # Вывод фильтра по категориям справа экрана с потомками родителя
    ),
    list_editable = (
        'is_active',
    ),
)

# Модель Значения в виде категорий
admin.site.register(
    Value,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        'attribute',
        #'parent',
        #'value',
        'is_active',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
    list_filter=(
        #'name',       # Вывод фильтра по категориям справа экрана
        ('attribute', TreeRelatedFieldListFilter), # Вывод фильтра по категориям справа экрана с потомками родителя
    ),
    list_editable = (
        'is_active',
    ),
)

