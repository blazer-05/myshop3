from django.contrib import admin
from .models import Banners

class BannersAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'image_img', 'link', 'is_active', 'created', 'updated']
    list_editable = ['is_active',]
    list_display_links = ['title',]


admin.site.register(Banners, BannersAdmin)

