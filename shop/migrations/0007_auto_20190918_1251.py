# Generated by Django 2.0.6 on 2019-09-18 09:51

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_middlwarenotification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='value',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='attribute', chained_model_field='attribute', on_delete=django.db.models.deletion.CASCADE, to='shop.Value', verbose_name='Значение'),
        ),
    ]
