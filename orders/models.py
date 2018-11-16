from django.conf import settings
from django.db import models

from cart.models import Cart, CartProduct
from shop.models import Product

from model_utils import Choices  #https://django-model-utils.readthedocs.io/en/latest/utilities.html

STATUS = Choices(
    (0, 'registration', 'На регистрации'),
    (1, 'execution', 'На исполнении'),
    (2, 'executed', 'Исполнен')
)

BUYING_TYPE = Choices(
    (0, 'take_out', 'Самовывоз'),
    (1, 'delivery', 'Доставка')
)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Всего')
    first_name = models.CharField(max_length=250, verbose_name='Имя')
    last_name = models.CharField(max_length=250, verbose_name='Фамилия')
    phone = models.CharField(max_length=25, verbose_name='Телефон')
    address = models.CharField(max_length=250, verbose_name='Адрес', blank=True)
    buying_type = models.IntegerField(verbose_name='Тип заказа', choices=BUYING_TYPE, default=BUYING_TYPE.delivery)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    comment = models.TextField(verbose_name='Комментарий к заказу')
    status = models.IntegerField(choices=STATUS, default=STATUS.registration, verbose_name='Статус заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ №{0}'.format(str(self.id))

