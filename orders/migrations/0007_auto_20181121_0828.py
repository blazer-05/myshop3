# Generated by Django 2.0.6 on 2018-11-21 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20181121_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='buying_type',
            field=models.CharField(choices=[('take_out', 'Самовывоз'), ('delivery', 'Доставка')], default='take_out', max_length=100, verbose_name='Тип заказа'),
        ),
    ]
