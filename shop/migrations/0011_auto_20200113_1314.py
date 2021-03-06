# Generated by Django 2.0.6 on 2020-01-13 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20191227_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='product',
            name='vendor_code',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Артикул товара'),
        ),
    ]
