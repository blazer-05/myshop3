from decimal import Decimal

from django.db.models import Sum, F

from shop.models import Product
from django.db import models


class Cart(models.Model):
    products = models.ManyToManyField(Product, through='CartProduct')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return str(self.id)

    @property
    def total(self):
        t = self.cartproduct_set.aggregate(
            total=Sum(
                F('quantity') * F('product__price') * (100 - F('product__discount')) / 100,
                output_field=models.DecimalField(decimal_places=2))
        ).get('total') or Decimal(0)
        return t.quantize(Decimal('0.01'))

    @property
    def count(self):
        return self.products.count()


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return 'Cart item for product {0}'.format(self.product.title)

    @property
    def total(self):
        return self.quantity * self.product.get_sale()
