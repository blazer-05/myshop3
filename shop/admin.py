from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from mptt.admin import TreeRelatedFieldListFilter
from django_summernote.admin import SummernoteModelAdmin
from shop.models import Category, Brand, Product, ProductAlbomImages

from eav.forms import BaseDynamicEntityForm
from eav.admin import BaseEntityAdmin
# https://django-eav-2.readthedocs.io/en/improvement-docs/usage.html#admin-integration

class ProductAdminForm(BaseDynamicEntityForm):
    model = Product

class ProductAdmin(BaseEntityAdmin, SummernoteModelAdmin):
    form = ProductAdminForm
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

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']

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

class ProductAlbomImagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_img', 'product', 'is_activ', 'created', 'updated']
    readonly_fields = ['image_img']

admin.site.register(ProductAlbomImages, ProductAlbomImagesAdmin)