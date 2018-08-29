from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from mptt.admin import TreeRelatedFieldListFilter

from shop.models import Category, Brand, Product

# class CategoryAdmin(DraggableMPTTAdmin):
#     prepopulated_fields = {'slug': ('name',)}
#     list_display = ['name', 'slug', 'is_activ']
#     list_editable = ['slug', 'is_activ']

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'category', 'brand', 'slug', 'image_img', 'price', 'stock', 'is_activ', 'created', 'updated']
    readonly_fields = ['image_img', ] # Выводит в карточке товара картинку товара!
    list_filter = (#'category',
                   ('category', TreeRelatedFieldListFilter),
                   'brand',
                   'is_activ',
                   'created',
                   'updated'
                   )
    search_fields = ['title']
    list_editable = ['slug', 'is_activ']


#admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)

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
        'is_activ',
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
        'is_activ',
    ),
    readonly_fields = ['image_img', ], # Выводит в карточке товара картинку товара!
    prepopulated_fields = {'slug': ('name',)}, # Автозаполнение поля slug
    mptt_level_indent=20 # Эта настройка задает отступ субкатегории от родительской категории
)

