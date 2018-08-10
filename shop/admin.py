from django.contrib import admin
from shop.models import Category, Brand, Product

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug', 'is_activ']
    list_editable = ['slug', 'is_activ']

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'category', 'brand', 'slug', 'image_img', 'price', 'stock', 'is_activ', 'created', 'updated']
    readonly_fields = ['image_img', ] # Выводит в карточке товара картинку товара!
    #list_editable = ['slug', 'is_activ']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
