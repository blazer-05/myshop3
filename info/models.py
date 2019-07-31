from django.db import models
from model_utils import Choices  # https://django-model-utils.readthedocs.io/en/latest/utilities.html
from django.urls import reverse
from mptt.models import MPTTModel

from shop.models import Product
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


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
    ''' Для вывода колонки количества комментариев к статье в админке '''
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
    comments = GenericRelation('comments.comment')  # Обратная обобщенная связь на модель Comment
    is_active = models.BooleanField(default=False, verbose_name='Модерация')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    objects = NewsQuerySet.as_manager()     # Для вывода колонки количества комментариев к статье в админке

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


class Review(models.Model):
    '''Отзыв о товаре с оценкой'''

    '''Для вывода в шаблоне нужного значения
    https://djbook.ru/rel1.8/ref/models/instances.html#extra-instance-methods
    использовать get_period_display где period - это поле селекта в модели. 
    '''
    RATING_CHOICES = Choices(
        (1, 'terrible', 'Ужасно!'),
        (2, 'badly', 'Плохо'),
        (3, 'normally', 'Нормально'),
        (4, 'good', 'Хорошо'),
        (5, 'perfectly', 'Отлично!'),
    )

    PERIOD_OF_USE = Choices(
        (0, 'less_than_a_month', 'Меньше месяца'),
        (1, 'one_month', '1 Месяц'),
        (2, 'three_months', '3 Месяца'),
        (3, 'six_months', '6 Месяцев'),
        (4, 'one_year', '1 Год'),
        (5, 'more_than_a_year', 'Больше года'),
    )

    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE, verbose_name='Товар')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Пользователь')
    user_name = models.CharField(max_length=250, blank=True, verbose_name='Посетитель')
    city = models.CharField(max_length=200, blank=True, verbose_name='Ваш город')
    image = models.ImageField(upload_to='review/%y/%m/%d/', blank=True, verbose_name='Изображение')
    merits = models.TextField(verbose_name='Достоинства', blank=True)
    limitations = models.TextField(verbose_name='Недостатки', blank=True)
    comment = models.TextField(verbose_name='Текст отзыва', blank=True)
    email = models.EmailField(max_length=50, blank=True, verbose_name='e-mail')
    video = models.URLField(max_length=500, blank=True, verbose_name='Ссылка на видео')
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='Рейтинг', blank=True)
    period = models.IntegerField(choices=PERIOD_OF_USE, verbose_name='Период использования', blank=True)
    user_like = models.ManyToManyField(User, verbose_name='Кто поставил лайк', related_name='review_users_like', blank=True)
    user_dislike = models.ManyToManyField(User, verbose_name='Кто поставил дизлайк', related_name='review_users_dislike', blank=True)
    is_active = models.BooleanField(default=False, verbose_name='Модерация')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created']

    def __str__(self):
        return 'Отзыв к товару {} ({})'.format(self.product.title, self.get_rating_display())


    # Вывод картинок в админке!
    # Обязательно сделать импорт функции mark_safe() иначе вместо картинки будет выводить html код картинки.
    def image_img(self):
        if self.image:
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="80px" height="50px"/></a>'.format(self.image.url))
        else:
            return '(Нет изображения)'
    image_img.short_description = 'Картинка'
    image_img.allow_tags = True

