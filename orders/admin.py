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
        'delivery_date',
        'comment',
        'status',
        'date',
    ]

admin.site.register(Order, OrderAdmin)