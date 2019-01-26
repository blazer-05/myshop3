import mptt
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

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

class NewsQuerySet(models.QuerySet):
    '''Для вывода колонки количества комментариев к статье в админке'''
    def with_comments_count(self):
        return self.annotate(comments_count=models.Count('comments'))

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, verbose_name='Транслит')
    metakeywords = models.CharField(max_length=200, verbose_name='Ключевые слова', blank=True)
    metadescription = models.CharField(max_length=200, verbose_name='Описание', blank=True)
    text = models.TextField(verbose_name='Статья')
    images = models.ImageField(upload_to='news/%y/%m/%d/', blank=True, verbose_name='Изображение статьи')
    video = models.URLField(blank=True, verbose_name='Ссылка на видео')
    count = models.IntegerField(default=0, verbose_name='Просмотры')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    is_active = models.BooleanField(default=False, verbose_name='Модерация')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    objects = NewsQuerySet.as_manager()     #'''Для вывода колонки количества комментариев к статье в админке'''
    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'
        ordering = ['-created']


    def __str__(self):
        return self.title

    # Вывод картинок в админке!
    # Обязательно сделать импорт функции mark_safe() иначе вместо картинки будет выводить html код картинки.
    def image_img(self):
        if self.images:
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="80px" height="50px"/></a>'.format(self.images.url))
        else:
            return '(Нет изображения)'
    image_img.short_description = 'Картинка'
    image_img.allow_tags = True

    def get_absolute_url(self):
        return reverse('news:newsdetails', kwargs={'slug': self.slug})

class Comment(MPTTModel):
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name='Родительская категория', related_name='children', on_delete=models.CASCADE, editable=False) # editable=False (Скрыл поле parent в админке)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='Новость')
    text = models.TextField(verbose_name='Комментарий')
    email = models.EmailField(max_length=50, blank=True, verbose_name='e-mail')
    user_name = models.CharField(max_length=100, blank=True, verbose_name='Логин пользователя')
    like = models.IntegerField(default=0, verbose_name='like')
    dislike = models.IntegerField(default=0, verbose_name='dislike')
    count_comment = models.IntegerField(default=0, verbose_name='Количество комментариев')
    is_active = models.BooleanField(default=False, verbose_name='Модерация')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ['-created']

    def __str__(self):
        return '{} {}'.format(self.user, self.news)
