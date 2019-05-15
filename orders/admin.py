from django.contrib import admin
from orders.models import Order
from cart.models import Cart, CartProduct


# class CartProductItemInline(admin.TabularInline):
#     model = CartProduct
#     raw_id_field = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'cart',
        'sender',
        'is_authenticated',
        'total',
        'full_name',
        'phone',
        'address',
        'buying_type',
        'delivery_date',
        'comment',
        'status',
        'date',
    ]

    list_display_links = ['sender']
    #inlines = [CartProductItemInline]

    def sender(self, obj):
        '''Метод определяет в одном столбце кто добавил комментарий user или user_name (т.е. зарегистрированный или нет пользовватель)'''
        return obj.user or obj.full_name

    sender.short_description = 'Отправитель'

    def is_authenticated(self, obj):
        '''Метод определяет в одном столбце от кого был комментарий от авторизаванного или анонимного пользователя'''
        return bool(obj.user)

    is_authenticated.short_description = 'Зарегистрирован'
    is_authenticated.boolean = True

    def change_view(self, request, object_id, form_url='', extra_context=None):
        '''Метод для вывода заказанных товаров (шаблон - orders/templates/admin/orders/order/change_form.html),
        выводится в теле заказа
        '''
        extra_context = {'cart_product_qs': CartProduct.objects.filter(cart__order=object_id)}
        return super().change_view(request, object_id, form_url, extra_context)


admin.site.register(Order, OrderAdmin)
# admin.site.register(CartProduct, CartProductItemInline)

