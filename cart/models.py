from shop.models import *
from django.db import models


# Промежуточная модель продукта который будет попадать в корзину
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество')
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Кол-во товара в корзине')

    def __str__(self):
        return 'Cart item for product {0}'.format(self.product.title)

# Модель корзины
class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Итоговая сумма заказа')

    def add_to_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
        cart_items = [item.product for item in cart.items.all()]
        if new_item.product not in cart_items:
            cart.items.add(new_item)
            cart.save()

    def remove_from_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        for cart_item in cart.items.all():
            if cart_item.product == product:
                cart.items.remove(cart_item)
                cart.save()

    def __str__(self):
        return str(self.id) # Возвращаем id корзины