from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from mptt.admin import DraggableMPTTAdmin
from mptt.admin import TreeRelatedFieldListFilter

from shop.models import (
    Category,
    Brand,
    Product,
    ProductAlbomImages,
    Attribute,
    Value,
    Entry,
    CategoryIndexPage,
    Bestseller,
    SaleCategory,
    SaleProduct,
    MiddlwareNotification,
    )

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


class AlbomInLine(admin.TabularInline):
    model = ProductAlbomImages
    readonly_fields = ['image_img']
    fields = ['image_img', 'name', 'image', 'parent', 'is_active'] # Порядок вывода объектов в карточке товара слева направо.
    #raw_id_fields = ('product',)
    extra = 0 # Количество видимых полей для добавления картинки


class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'image_img', 'slug', 'description', 'is_active', 'created', 'updated']
    readonly_fields = ['image_img', ] # Выводит в карточке товара картинку товара!
    actions = [complete_post, incomplete_post]


# Класс модели Entry для вывода атрибута и значения
class EntryInline(admin.TabularInline):
    model = Entry
    fields = ('attribute', 'value', 'is_active')
    #raw_id_fields = ('attribute', 'value',)
    extra = 0 # Количество видимых полей для добавления атрибут/значения


# Класс модели продукта
class ProductAdmin(SummernoteModelAdmin):
    inlines = [EntryInline, AlbomInLine] # Привязываем модель EntryInline в админке к товару.
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'vendor_code', 'category', 'brand', 'slug', 'image_img', 'price', 'stock', 'is_active', 'created', 'updated']
    readonly_fields = ['image_img', ] # Выводит в карточке товара картинку товара!
    list_filter = (#'category',
                   ('category', TreeRelatedFieldListFilter),
                   'brand',
                   'is_active',
                   'created',
                   'updated',

                   )
    search_fields = ['title', 'vendor_code']
    list_editable = ['slug', 'is_active', 'stock',]
    list_per_page = 10  # Вывод количества новостей в админке
    actions = [complete_post, incomplete_post] # Методы complete_post, incomplete_post для массового снятия/публикации товаров.


admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(MiddlwareNotification)


# Класс модели блока SaleProduct
admin.site.register(
    SaleProduct,
    DraggableMPTTAdmin,
    list_display = (
        'tree_actions',
        'indented_title',
        #'sale_product',
        'is_active',
    ),
    list_editable = (
        'is_active',
    ),
    actions = [complete_post, incomplete_post], # Методы complete_post, incomplete_post для массового снятия/публикации товаров.
    fields = ('sale_product', 'is_active'), # Задает в админке в каком порядке будут выстроенны поля.(В данном случае сначала категории потом продукты)
    #list_display_links = ['sale_product'] # Задает в админке ссылку на объект

)

# Класс модели блока SaleCategory
admin.site.register(
    SaleCategory,
    DraggableMPTTAdmin,
    list_display = (
        'tree_actions',
        'indented_title',
        #'sale_category',
        'is_active',
    ),
    list_editable = (
        'is_active',
    ),
    actions = [complete_post, incomplete_post], # Методы complete_post, incomplete_post для массового снятия/публикации товаров.
    fields = ('sale_category', 'is_active'), # Задает в админке в каком порядке будут выстроенны поля.(В данном случае сначала категории потом продукты)
    #list_display_links = ['sale_category'] # Задает в админке ссылку на объект

)

# Блок Bestseller
admin.site.register(
    Bestseller,
    DraggableMPTTAdmin,
    list_display = (
        'tree_actions',
        'indented_title',
        #'bestseller',
        'is_active',
    ),
    list_editable = (
        'is_active',
    ),
    actions = [complete_post, incomplete_post] # Методы complete_post, incomplete_post для массового снятия/публикации товаров.
)

# Вывод категорий и товаров на главной
admin.site.register(
    CategoryIndexPage,
    DraggableMPTTAdmin,
    list_display = (
        'tree_actions',
        'indented_title',
        #'sortcategory',
        'is_active',
    ),
    list_editable = (
        'is_active',
    )
)


# Модель Фото альбома в виде категорий
admin.site.register(
    ProductAlbomImages,
    DraggableMPTTAdmin,
    list_display = (
        'tree_actions',
        'indented_title',
        #'name',
        'image_img',
        'product',
        'is_active',
        'created',
        'updated'
    ),
    list_editable = (
      'is_active',
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
    # filter_horizontal = (
    #     'attributes',
    # ),
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

