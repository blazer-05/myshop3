from django.db import models
from model_utils import Choices


class NewsletterUser(models.Model):
    '''Модель email подписки'''
    name = models.CharField(max_length=250, blank=True, verbose_name='ФИО')
    email = models.EmailField(verbose_name='email')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    '''Рассылка сообщений'''
    EMAIL_STATUS_CHOICES = Choices(
        (1, 'Draft', 'Черновик'),
        (2, 'Published', 'Опубликовано')
    )

    subject = models.CharField(max_length=250, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержимое')
    users_email = models.ManyToManyField(NewsletterUser, verbose_name='email')
    status = models.IntegerField(choices=EMAIL_STATUS_CHOICES, verbose_name='Статус')
    file = models.FileField(upload_to='newsletter_files/%Y/%m/%d', blank=True, verbose_name='Файл')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return self.subject