import mptt
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
class Product(models.Model):
    category = TreeForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, verbose_name='Бренд', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, unique=True, verbose_name='Название товара')
    slug = models.SlugField()
    descriptions = models.TextField(blank=True, verbose_name='Описание')
    descriptions_two = models.TextField(blank=True, verbose_name='Доп.описание')
    images = models.ImageField(upload_to=image_folder, blank=True, verbose_name='Изображение товара')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    discount = models.IntegerField(default=0, verbose_name='Скидка')
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


    # Расчет скидки
    def get_sale(self):
        '''Расчитать стоимость со скидкой'''
        price = int(self.price * (100 - self.discount) / 100)
        return price

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


# Модель атрибута товара
class Attribute(MPTTModel):
    title = models.CharField(max_length=250, verbose_name='Атрибут')
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name='Родительская категория', related_name='children', on_delete=models.CASCADE)
    is_activ = models.BooleanField(default=True, verbose_name='Модерация')

    class Meta:
        verbose_name = 'Атрибут'
        verbose_name_plural = 'Атрибуты'

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']


mptt.register(Attribute, order_insertion_by=['title'])

# Модель значения товара связанная с моделью атрибута
class Value(MPTTModel):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name='Атрибут')
    value = models.CharField(max_length=250, blank=True, verbose_name='Значение')
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name='Родительская категория', related_name='children', on_delete=models.CASCADE, editable=False) # editable=False (Скрыл поле parent в админке)
    is_activ = models.BooleanField(default=True, verbose_name='Модерация')

    class Meta:
        verbose_name = 'Значение'
        verbose_name_plural = 'Значения'

    def __str__(self):
        return self.value

    class MPTTMeta:
        order_insertion_by = ['value']


mptt.register(Value, order_insertion_by=['value'])

# Модель связанная с продуктом, атрибутом и значением. Выводится под товаром.
class Entry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.ForeignKey(Value, on_delete=models.CASCADE)
    is_activ = models.BooleanField(default=True, verbose_name='Модерация')

    def __str__(self):
        return '{} - {}'.format(self.attribute.title, self.value.value)