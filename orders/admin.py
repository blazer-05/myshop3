from django.contrib import admin

from orders.models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'cart',
        'total',
        'first_name',
        'last_name',
        'phone',
        'address',
        'buying_type',
        'date',
        'comment',
        'status'
    ]

admin.site.register(Order, OrderAdmin)