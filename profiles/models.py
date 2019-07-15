from PIL import Image
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from shop.models import Product


class Profile(models.Model):
    """Модель профиля пользователя"""
    user = models.OneToOneField(User, unique=True, verbose_name="Пользователь", on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, verbose_name='Продукты')
    first_name = models.CharField(max_length=50, verbose_name="Имя", blank=True)
    last_name = models.CharField(max_length=50, verbose_name="Фамилия", blank=True)
    avatar = models.ImageField(upload_to="profile/avatar/%y/%m/%d/", blank=True, verbose_name="Аватар")
    phone = models.CharField(max_length=25, verbose_name="Телефон", blank=True)
    date_birth = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name='Город', blank=True)
    slug = models.SlugField("URL", max_length=100, default='')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models. DateTimeField(auto_now=True, verbose_name='дата обновления')
    is_active = models.BooleanField(default=True, verbose_name='Модерация')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профиля"

    def avatar_img(self):
        if self.avatar:
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="50px" height="50px"/></a>'.format(self.avatar.url))
        else:
            return '(Нет изображения)'
    avatar_img.short_description = 'Картинка'
    avatar_img.allow_tags = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 100 or img.width > 100:
                output_size = (100, 100)
                img.thumbnail(output_size)
                img.save(self.avatar.path)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создание профиля пользователя при регистрации
    (данные полей first_name и last_name сохраняются в модель профиля )"""
    if created:
        Profile.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name)


@receiver
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
