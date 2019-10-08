import mptt
import random
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Avg, Q, Count, Exists, OuterRef, Value as ExpressionValue
from django.db.models.signals import post_save

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe # Импорт функции для вывода в админке картинок.
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.core.mail import EmailMultiAlternatives
from requests import request

from myshop3.settings import site_url
from myshop3 import local_settings
from django.utils import timezone
from decimal import Decimal

from notifications.signals import notify
from smart_selects.db_fields import ChainedForeignKey


class Category(MPTTModel):
    '''Категории'''
    name = models.CharField(max_length=250, unique=True, verbose_name='Катагория')
    slug = models.SlugField(max_length=250, verbose_name='Транслит')
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name='Родительская категория', related_name='children', on_delete=models.CASCADE)
    description = models.TextField(blank=True, verbose_name='Описание')
    img = models.ImageField(upload_to='img_category/%y/%m/%d/', blank=True, verbose_name='Изображение категории')
    attributes = models.ManyToManyField('Attribute', blank=True, verbose_name='Атрибуты товара')
    is_active = models.BooleanField(default=True, verbose_name='Модерация')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Отредактирован')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('tree_id', 'level')

    def __str__(self):
        return self.name

    # Возвращает ссылку на категорию в шаблоне главной страницы index {{ category.sortcategory.get_absolut_url }}
    def get_absolute_url(self):
        return reverse('shop:shop-list', kwargs={'slug': self.slug})

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


class Brand(models.Model):
    '''Бренды'''
    name = models.CharField(max_length=200, blank=True, unique=True, verbose_name='Бренд')
    slug = models.SlugField(max_length=200, verbose_name='Транслит')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='img_brand/%y/%m/%d/', blank=True, verbose_name='Изображение')
    is_active = models.BooleanField(default=True, verbose_name='Модерация')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Отредактирован')

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name']

    def __str__(self):
        return self.name

    def image_img(self):
        if self.image:
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.image.url))
        else:
            return '(Нет изображения)'
    image_img.short_description = 'Картинка'
    image_img.allow_tags = True

# Функция, которая переопределяет имя картинки на то что мы пишем в поле slug для удобо-читаемости
# Вывожу эту функцию в моделе товара в поле images upload_to=image_folder
# def image_folder(instance, filename):
#     filename = instance.slug + '.' + filename.split('.')[1]
#     return '{0}/{1}'.format(instance.slug, filename)


class ProductQueryset(models.QuerySet):
    '''Класс кверисета для модели Product - для вывода рейтинга в шаблонах сайта'''

    '''Метод with_rating() - выводит количество звезд. Добавлен в словари методов get_index_categories,get_bestseller_category,get_sale_category
       в шаблоне index.html рейтинг звезд выводится переменной product.rating. Добавлен во вьюху productdetails
       Product.objects.with_rating() и выводит в шаблоне product-details.html звезды {% if forloop.counter <= product.rating %}
    '''
    def with_rating(self):
        return self.annotate(rating=Avg('reviews__rating', filter=Q(reviews__is_active=True)))

    '''Метод with_review_count() используется во вьюхе productdetails и в шаблоне product-details.html
       {{ product.review_count }} выводит общее количество отзывов. 
    '''
    def with_review_count(self):
        return self.annotate(review_count=Count('reviews__rating', filter=Q(reviews__is_active=True)))

    '''Метод with_in_wishlist используется для вишлиста, при добавлении товара в вишлист кнопка имеет вид красного
    цвета 
    '''
    def with_in_wishlist(self, user):
        if user.is_authenticated:
            return self.annotate(
                in_wishlist=Exists(
                    user.profile.products.filter(pk=OuterRef('pk'))
                )
            )
        else:
            return self.annotate(
                in_wishlist = ExpressionValue(False, output_field=models.BooleanField())
            )


class Product(models.Model):
    '''Модель продукта'''
    category = TreeForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, blank=True, null=True, verbose_name='Бренд', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, unique=True, verbose_name='Название товара')
    slug = models.SlugField(verbose_name='Транслит')
    meta_keywords = models. CharField(max_length=250, blank=True, verbose_name='Клюевые слова')
    meta_descriptions = models.CharField(max_length=250, blank=True, verbose_name='Мета описание')
    descriptions = models.TextField(blank=True, verbose_name='Описание')
    descriptions_two = models.TextField(blank=True, verbose_name='Доп.описание', editable=False) # Скрыл это поле в админке атрибутом editable=False
    images = models.ImageField(upload_to='img_product/%y/%m/%d/', blank=True, verbose_name='Изображение товара')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    discount = models.IntegerField(default=0, verbose_name='Скидка')
    new = models.BooleanField(default=False, verbose_name='Новый товар')
    akciya = models.BooleanField(default=False, verbose_name='Акция')
    akciya_text = models.TextField(blank=True, verbose_name='Описание')
    timer = models.BooleanField(default=False, verbose_name='Таймер')
    timer_before = models.DateTimeField(null=True, blank=True, verbose_name='Дата таймера')
    stock = models.PositiveIntegerField(verbose_name='Количество')
    vendor_code = models.IntegerField(default=0, verbose_name='Артикул товара')
    is_active = models.BooleanField(default=True, verbose_name='Модерация')
    comments = GenericRelation('comments.comment')  # Обратная обобщенная связь на модель Comment
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Отредактирован')
    objects = ProductQueryset.as_manager() # Относится к классу ProductQueryset

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created']

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
        return reverse('shop:product-details', kwargs={'product_slug': self.slug})

    def get_sale(self):
        '''Расчитать стоимость со скидкой'''
        price = Decimal(self.price * (100 - self.discount) / 100)
        return price

    def need_timer(self):
        '''Таймер для акции'''
        return self.timer and self.timer_before and timezone.now() < self.timer_before

    def generate_vendor_code(self, numbers=5):
        '''Переопределен метод save() для генерации случайных чисел для поля vendor_code (Артикул товара),
        в параметре numbers=6 можно задать количество чисел.
        '''
        while not self.vendor_code:
            vendor_code = random.randint(10**numbers, 10**(numbers+1) - 1)
            if not Product.objects.filter(vendor_code=vendor_code).exists():
                self.vendor_code = vendor_code

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.generate_vendor_code()
        super().save(force_insert, force_update, using, update_fields)


def email_send_notify_to_user(user, product):
    '''Отправка пользователю уведомление на емейл о поступлении товара на который был подписан пользователь '''
    subject = 'Уведомление о поступившем товаре "{}"'.format(product.title)
    from_email = local_settings.DEFAULT_FROM_EMAIL
    body = 'Товар {}появился в продаже'.format(product.title)
    to_email = user.email
    notify_messages = EmailMultiAlternatives(subject=subject, body=body, from_email=from_email, to=[to_email])
    context = {
        'user': user,
        'product': product,
        'site_url': site_url,
    }
    user_message = render_to_string('shop/notification/notify.html', context)
    notify_messages.attach_alternative(user_message, 'text/html')
    notify_messages.send()


def product_available_notification(sender, instance, *args, **kwargs):
    '''Сигнал отвечающий за доставку нотификации'''
    if instance.stock:
        await_for_notify = [notification for notification in MiddlwareNotification.objects.filter(
            product=instance)]
        for notification in await_for_notify:
            email_send_notify_to_user(notification.user_name, instance) # вызов метода email_send_notify_to_user
            notify.send(
                instance,
                recipient=[notification.user_name],
                verb='Уважаемый {0}! {1}, который Вы ждете, поступил'.format(
                    notification.user_name.username,
                    instance.title),
                description=instance.slug,
                )
            notification.delete()


post_save.connect(product_available_notification, sender=Product)


# Модель альбома с изображениями для товаров
class ProductAlbomImages(MPTTModel):
    name = models.CharField(max_length=200, verbose_name='Название')
    product = models.ForeignKey(Product, blank=True, null=True, related_name='image', on_delete=models.CASCADE, verbose_name='Продукт')
    image = models.ImageField(upload_to='product-albom-images/%y/%m/%d/', blank=True, verbose_name='Загрузить картинку')
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name='Родительская категория', related_name='children', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, verbose_name='Модерация')
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
    is_active = models.BooleanField(default=True, verbose_name='Модерация')
    is_filter = models.BooleanField(default=False, verbose_name='Фильтр')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Отредактирован')

    class Meta:
        verbose_name = 'Атрибут'
        verbose_name_plural = 'Атрибуты товара'

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']


mptt.register(Attribute, order_insertion_by=['title'])


# Модель значения товара связанная с моделью атрибута
class Value(MPTTModel):
    attribute = models.ForeignKey(Attribute, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Атрибут')
    value = models.CharField(max_length=250, blank=True, verbose_name='Значение')
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name='Родительская категория', related_name='children', on_delete=models.CASCADE) # editable=False (Скрыл поле parent в админке)
    is_active = models.BooleanField(default=True, verbose_name='Модерация')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Отредактирован')

    class Meta:
        verbose_name = 'Значение'
        verbose_name_plural = 'Значения'

    def __str__(self):
        return self.value

    class MPTTMeta:
        order_insertion_by = ['value']


mptt.register(Value, order_insertion_by=['value'])


# Для работы булевого is_activ нужно для модели Entry создать этот кверисет в котором метод activ возвращает по фильтру is_activ
# Далее в модели Entry добавляем менеджер сделанный из этого кверисета objects = EntryQuerySet.as_manager(). В шаблоне product-details.html
# проходимся циклом по этой переменной product.entry_set.active ({% for entry in product.entry_set.active %}) Таким образом во вьюхе productdetails
# не нужно получать Entry из модели и обрабатывать ее. Будет корректно работать булево значение is_activ напрямую в шаблон без вьюхи.
class EntryQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


# Модель связанная с продуктом, атрибутом и значением. Выводится под товаром.
class Entry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name='Атрибут')

    '''Это поле "value" используется внешней библиотекой Django Smart Selects 1.5.3 В админке к товару в модели Entry
    в выпадающем списке "Значение" упорядочевает значения принадлежащие только тем атрибутам товара которые заданы для этой категории товара
    в разделе "Категории".
    Т.е. все другие значения для других товаров отфильтровываются автоматически и остаются только те которые принадлежат атрибутам данного товара.'''
    value = ChainedForeignKey(
        Value,
        chained_field="attribute",
        chained_model_field="attribute",
        show_all=False,
        auto_choose=True,
        sort=True,
        verbose_name='Значение',
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True, verbose_name='Модерация')
    objects = EntryQuerySet.as_manager()
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Отредактирован')

    def __str__(self):
        return '{} - {}'.format(self.attribute.title, self.value.value)


# Модель и метод для вывода на главной всех товаров принадлежайших каждый своей категории в рандомном порядке (.order_by('?')[:10]).
class CategoryIndexPage(MPTTModel):
    sortcategory = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Вывод категорий на главной странице')
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name='Родительская категория', related_name='children', on_delete=models.CASCADE, editable=False)  # editable=False (Скрыл поле parent в админке)
    brands = models.ManyToManyField(Brand, blank=True, verbose_name='Сортировать по брендам')
    is_active = models.BooleanField(default=True, verbose_name='Модерация')

    class Meta:
        verbose_name = 'Вывод из категории на главной'
        verbose_name_plural = 'Вывод из категорий на главной'

    def __str__(self):
        return '{}'.format(self.sortcategory)

    @classmethod
    def get_index_categories(cls, user):
        index_categories = {}
        for category in cls.objects.filter(is_active=True):
            cat_descendants = category.sortcategory.get_descendants(include_self=True)
            index_categories.update(
                {category: Product.objects.filter(category__in=cat_descendants, is_active=True).order_by('?').with_rating().with_in_wishlist(user)[:10]}
            )
        return index_categories
    '''
    # .with_rating() для вывода на главной звезд рейтинга. 
    # .with_in_wishlist(user) для вывода на главной и др.стр. кнопки вишлиста
    '''


# Модель и метод для вывода на главной в блоке bestseller всех товаров принадлежайших каждый своей категории в рандомном порядке (.order_by('?')[:4]).
class Bestseller(MPTTModel):
    bestseller = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Выберите категорию')
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name='Родительская категория', related_name='children', on_delete=models.CASCADE, editable=False)  # editable=False (Скрыл поле parent в админке)
    is_active = models.BooleanField(default=True, verbose_name='Модерация')

    class Meta:
        verbose_name = 'Бестселлер'
        verbose_name_plural = 'Блок Бестселлеры'

    def __str__(self):
        return '{}'.format(self.bestseller)

    @classmethod
    def get_bestseller_category(self):
        bestseller_categories = {}
        for category in self.objects.filter(is_active=True):
            #best_descendants = category.bestseller.get_descendants(include_self=True) # Тут товары отсортированы по категориям
            bestseller_categories.update(
                {category: Product.objects.filter(is_active=True).order_by('?').with_rating()[:4]} # category__in=best_descendants #.with_rating() для вывода на главной звезд рейтинга
            )
        return bestseller_categories


# Модель и метод вывода на главной товаров по категориям в блоке распродажа
class SaleCategory(MPTTModel):
    sale_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Выберите категорию')
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name='Родительская категория', related_name='children', on_delete=models.CASCADE, editable=False)  # editable=False (Скрыл поле parent в админке)
    is_active = models.BooleanField(default=True, verbose_name='Модерация')

    class Meta:
        verbose_name = 'Распродажа по категориям'
        verbose_name_plural = 'Распродажи по категориям'

    def __str__(self):
        return '{}'.format(self.sale_category)

    @classmethod
    def get_sale_category(self, user):
        sale_categories = {}
        for category in self.objects.filter(is_active=True):
            sale_descendants = category.sale_category.get_descendants(include_self=True) # Тут товары отсортированы по категориям
            sale_categories.update(
                {category: Product.objects.filter(category__in=sale_descendants, is_active=True).order_by('?').with_rating().with_in_wishlist(user)[:9]} # category__in=best_descendants # .with_rating() для вывода на главной звезд рейтинга
            )
        return sale_categories


# Модель и метод вывода на главной товаров по штучно в блоке распродажа
class SaleProduct(MPTTModel):
    sale_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Выберите товар')
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name='Родительская категория', related_name='children', on_delete=models.CASCADE, editable=False)  # editable=False (Скрыл поле parent в админке)
    is_active = models.BooleanField(default=True, verbose_name='Модерация')

    class Meta:
        verbose_name = 'Распродажа по товарам'
        verbose_name_plural = 'Распродажи по товарам'

    def __str__(self):
        return '{}'.format(self.sale_product)

    @classmethod
    def get_sale_product(cls, user):
        return Product.objects.filter(
            is_active=True,
            pk__in=cls.objects.filter(is_active=True).values_list('sale_product')
        ).with_rating().with_in_wishlist(user)

    # @classmethod
    # def get_sale_product(self):
    #     return self.objects.filter(is_active=True) # Получаем все товары выбранные в админке


class MiddlwareNotification(models.Model):
    '''Нотификация о поступлении товара'''
    user_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    is_notified = models.BooleanField(default=False, verbose_name='Нотификация')

    class Meta:
        verbose_name = 'Нотификация'
        verbose_name_plural = 'Нотификации'

    def __str__(self):
        return 'Нотификация для пользователя "{0}" о поступлении товара "{1}"'.format(self.user_name.username, self.product.title)


class PriceList(models.Model):
    '''Модель прайс листа'''
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    file = models.FileField(upload_to='price_list/%y/%m/%d/', verbose_name='Файл')
    counter = models.PositiveIntegerField(default=0, verbose_name='Кол-во загрузок')
    is_active = models.BooleanField(default=True, verbose_name='Модерация')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменен')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Прайс лист'
        verbose_name_plural = 'Прайс листы'
        ordering = ['-created']