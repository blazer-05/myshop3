from django.conf import settings
from django.db import models

from cart.models import *
from shop.models import *

ORDER_STATUS_CHAICES = (
    ('Принят в обработку', 'Принят в обработку'),
    ('Выполняется', 'Выполняется'),
    ('Оплачен', 'Оплачен')
)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    items = models.ManyToManyField(Cart, verbose_name='Товар')
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Всего')
    first_name = models.CharField(max_length=250, verbose_name='Имя')
    last_name = models.CharField(max_length=250, verbose_name='Фамилия')
    phone = models.CharField(max_length=25, verbose_name='Телефон')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    buying_type = models.CharField(max_length=50, verbose_name='Тип заказа', choices=(('Самовывоз', 'Самовывоз'), ('Доставка', 'Доставка')))
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    comments = models.TextField(verbose_name='Комментарий к заказу')
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHAICES, verbose_name='Статус заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ №{0}'.format(str(self.id))

