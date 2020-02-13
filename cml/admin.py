from __future__ import absolute_import
from django.contrib import admin
from .models import *


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):

    list_display = ('exchange_type', 'timestamp', 'user', 'filename')
    readonly_fields = ('exchange_type', 'timestamp', 'user', 'filename')
    list_per_page = 20

    def has_add_permission(self, request):
        return False
