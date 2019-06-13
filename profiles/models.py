from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    """Модель профиля пользователя"""
    user = models.OneToOneField(User, unique=True, verbose_name="Пользователь", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name="Имя", blank=True)
    last_name = models.CharField(max_length=50, verbose_name="Фамилия", blank=True)
    avatar = models.ImageField(upload_to="profile/avatar/%y/%m/%d/", blank=True, verbose_name="Аватар")
    email_two = models.EmailField(verbose_name="Доп. email", blank=True)
    phone = models.CharField(max_length=25, verbose_name="Телефон", blank=True)
    date_birth = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    slug = models.SlugField("URL", max_length=50, default='')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models. DateTimeField(auto_now=True, verbose_name='дата обновления')
    is_active = models.BooleanField(default=True, verbose_name='Модерация')

    def __str__(self):
        return self.user.username


    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профиля"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создание профиля пользователя при регистрации"""
    if created:
        Profile.objects.create(user=instance)


@receiver
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
