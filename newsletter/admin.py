from django.contrib import admin

from .models import NewsletterUser, Newsletter


@admin.register(NewsletterUser)
class NewsletterUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'created']


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    pass
