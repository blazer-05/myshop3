from django.db import models
from django.utils.safestring import mark_safe


class Banners(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название баннера')
    description = models.TextField(blank=True, verbose_name='Описание баннера')
    images = models.ImageField(upload_to='img_banners/%y/%m/%d/', verbose_name='Изображение баннера')
    link = models.URLField(max_length=250, blank=True, verbose_name='Ссылка')
    is_active = models.BooleanField(default=False, verbose_name='Модерация')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Отредактирован')

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def __str__(self):
        return self.title

    # Вывод картинок в админке!
    # Обязательно сделать импорт функции mark_safe() иначе вместо картинки будет выводить html код картинки.
    def image_img(self):
        if self.images:
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100%" height="100%"/></a>'.format(self.images.url))
        else:
            return '(Нет изображения)'
    image_img.short_description = 'Картинка'
    image_img.allow_tags = True
