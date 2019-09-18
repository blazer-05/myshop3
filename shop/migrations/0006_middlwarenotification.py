# Generated by Django 2.0.6 on 2019-09-11 06:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0005_category_attributes'),
    ]

    operations = [
        migrations.CreateModel(
            name='MiddlwareNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_notified', models.BooleanField(default=False, verbose_name='Нотификация')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product', verbose_name='Продукт')),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Нотификации',
                'verbose_name': 'Нотификация',
            },
        ),
    ]
