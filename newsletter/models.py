from django.db import models


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