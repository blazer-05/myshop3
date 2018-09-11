import mptt
from eav.decorators import register_eav

from django.db import models
from django.utils.safestring import mark_safe # Импорт функции для вывода в админке картинок.
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


# Модель категорий
class Category(MPTTModel):
    name = models.CharField(max_length=250, unique=True, verbose_name='Катагория')
    slug = models.SlugField(max_length=250, verbose_name='Транслит')
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name='Родительская категория', related_name='children', on_delete=models.CASCADE)
    description = models.TextField(blank=True, verbose_name='Описание')
    img = models.ImageField(upload_to='img_category/%y/%m/%d/', blank=True, verbose_name='Изображение категории')
    is_activ = models.BooleanField(default=True, verbose_name='Модерация')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('tree_id', 'level')

    def __str__(self):
        return self.name

    # Вывод картинок в админке!
    # Обязательно сделать импорт функции mark_safe() иначе вместо картинки будет выводить html код картинки.
    def image_img(self):
        if self.img:
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.img.url))
        else:
            return '(Нет изображения)'
    image_img.short_description = 'Картинка'
    image_img.allow_tags = True

    class MPTTMeta:
        order_insertion_by = ['name']


mptt.register(Category, order_insertion_by=['name'])

# Модель брендов
class Brand(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Бренд')

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name']

    def __str__(self):
        return self.name

# Функция, которая переопределяет имя картинки на то что мы пишем в поле slug для удобо-читаемости
# Вывожу эту функцию в моделе товара в поле images upload_to=image_folder
def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return '{0}/{1}'.format(instance.slug, filename)

# Модель товара
@register_eav()
class Product(models.Model):
    category = TreeForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, verbose_name='Бренд', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, unique=True, verbose_name='Название товара')
    slug = models.SlugField()
    descriptions = models.TextField(verbose_name='Описание')
    images = models.ImageField(upload_to=image_folder, blank=True, verbose_name='Изображение товара')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    stock = models.PositiveIntegerField(verbose_name='Количество')
    is_activ = models.BooleanField(default=True, verbose_name='Модерация')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Отредактирован')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['title']

    def __str__(self):
        return self.title

    # Вывод картинок в админке!
    # Обязательно сделать импорт функции mark_safe() иначе вместо картинки будет выводить html код картинки.
    def image_img(self):
        if self.images:
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.images.url))
        else:
            return '(Нет изображения)'
    image_img.short_description = 'Картинка'
    image_img.allow_tags = True


    def get_absolute_url(self):
        return reverse('shop:product-details', kwargs={'product_slug': self.slug, 'albom_id': self.id})

# Модель альбома с изображениями для товаров
class ProductAlbomImages(models.Model):
    name = models.CharField(max_length=200, blank=True, verbose_name='Название')
    product = models.ForeignKey(Product, related_name='image', on_delete=models.CASCADE, verbose_name='Продукт')
    image = models.ImageField(upload_to='product-albom-images/%y/%m/%d/', blank=True, verbose_name='Фото товара')
    is_activ = models.BooleanField(default=True, verbose_name='Модерация')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Отредактирован')

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'

    def __str__(self):
        return self.name

    # Обязательно сделать импорт функции mark_safe() иначе вместо картинки будет выводить html код картинки.
    def image_img(self):
        if self.image:
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.image.url))
        else:
            return '(Нет изображения)'
    image_img.short_description = 'Картинка'
    image_img.allow_tags = True

