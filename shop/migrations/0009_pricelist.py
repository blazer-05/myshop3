# Generated by Django 2.0.6 on 2019-10-04 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_attribute_is_filter'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок')),
                ('file', models.FileField(upload_to='price_list/%y/%m/%d/', verbose_name='Файл')),
                ('counter', models.PositiveIntegerField(default=0, verbose_name='Кол-во загрузок')),
                ('is_active', models.BooleanField(default=True, verbose_name='Модерация')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Изменен')),
            ],
            options={
                'verbose_name': 'Прайс лист',
                'verbose_name_plural': 'Прайс листы',
                'ordering': ['-created'],
            },
        ),
    ]
