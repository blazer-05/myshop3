from django.db import models


class Contacts(models.Model):
    '''Форма обратной связи'''
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    phone = models.CharField(max_length=100, blank=True, verbose_name='Телефон')
    email = models.EmailField(max_length=100, blank=True, verbose_name='email')
    text = models.TextField(max_length=1500, verbose_name='Сообщение')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-created']

    def __str__(self):
        return self.full_name


class Maps(models.Model):
    '''Вставка ссылки на карту панораму'''
    name = models.CharField(max_length=250, verbose_name='Название')
    maps = models.URLField(max_length=1000, verbose_name='Ссылка')
    is_active = models.BooleanField(default=True, verbose_name='Модерация')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    update = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'
        ordering = ['-created']

    def __str__(self):
        return self.name


class About(models.Model):
    '''О магазине'''
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='О нас')
    is_active = models.BooleanField(default=True, verbose_name='Модерация')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    update = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О магазине'
        ordering = ['-created']

    def __str__(self):
        return self.title