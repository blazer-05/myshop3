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


class Address(models.Model):
    '''Контактные данные магазина'''
    title = models.CharField(max_length=150, blank=True, verbose_name='Заголовок')
    email_one = models.EmailField(max_length=100, blank=True, verbose_name='Email-1')
    email_two = models.EmailField(max_length=100, blank=True, verbose_name='Email-2')
    website = models.URLField(max_length=150, blank=True, verbose_name='Сайт')
    phone_one = models.CharField(max_length=100, blank=True, verbose_name='Телефон-1')
    phone_two = models.CharField(max_length=100, blank=True, verbose_name='Телефон-2')
    address = models.CharField(max_length=150, blank=True, verbose_name='Адрес')
    is_active = models.BooleanField(default=True, verbose_name='Модерация')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    update = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'
        ordering = ['-created']

    def __str__(self):
        return self.address


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


class PrivacyPolicy(models.Model):
    '''Политика конфиденциальности'''
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Модерация')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    update = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = 'Политика'
        verbose_name_plural = 'Политика'
        ordering = ['-created']

    def __str__(self):
        return self.title


class Delivery(models.Model):
    '''Информация о доставке товаров'''
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Модерация')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    update = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставка'
        ordering = ['-created']

    def __str__(self):
        return self.title


class Backcall(models.Model):
    '''Форма обратного звонка'''
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    phone = models.CharField(max_length=100, verbose_name='Телефон')
    text = models.TextField(max_length=1000, blank=True, verbose_name='Сообщение')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = 'Обратный звонок'
        verbose_name_plural = 'Обратный звонок'
        ordering = ['-created']

    def __str__(self):
        return self.full_name


class HeaderWidgetInfo(models.Model):
    '''Виджеты (working time, Free shipping, Money back 100%, Phone:) '''
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    text = models.CharField(max_length=50, verbose_name='Текст')

    class Meta:
        verbose_name = 'Виджет'
        verbose_name_plural = 'Виджеты'

    def __str__(self):
        return '{} - {}'.format(self.title, self.text)