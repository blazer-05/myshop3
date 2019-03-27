from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Comment(MPTTModel):
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name='Родительская категория', related_name='children', on_delete=models.CASCADE, editable=False) # editable=False (Скрыл поле parent в админке)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Комментарий')
    email = models.EmailField(max_length=50, blank=True, verbose_name='e-mail')
    user_name = models.CharField(max_length=100, blank=True, verbose_name='Логин пользователя')
    like = models.IntegerField(default=0, verbose_name='like')
    dislike = models.IntegerField(default=0, verbose_name='dislike')
    user_like = models.ManyToManyField(User, verbose_name='Кто поставил лайк', related_name='users_like', blank=True)
    user_dislike = models.ManyToManyField(User, verbose_name='Кто поставил дизлайк', related_name='users_dislike', blank=True)
    #count_comment = models.IntegerField(default=0, verbose_name='Количество комментариев')
    is_active = models.BooleanField(default=False, verbose_name='Модерация')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Создаем связь с внешней моделью ContentType.
    object_id = models.PositiveIntegerField()  # Содаем поле, которое будет хранить значения первичных ключей экземпляров модели с которой создана связь.
    content_object = GenericForeignKey('content_type', 'object_id')  # В это поле передаем в качестве аргументов, имена полей созданных ранее.

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ['-created']

    def __str__(self):
        return '{}'.format(self.content_object)
