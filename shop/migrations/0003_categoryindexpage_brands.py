# Generated by Django 2.0.6 on 2019-07-22 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20190121_0716'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoryindexpage',
            name='brands',
            field=models.ManyToManyField(to='shop.Brand', verbose_name='Сортировать по брендам'),
        ),
    ]