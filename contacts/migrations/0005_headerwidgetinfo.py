# Generated by Django 2.0.6 on 2019-11-21 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0004_auto_20190809_1254'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeaderWidgetInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок')),
                ('text', models.CharField(max_length=50, verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Виджет',
                'verbose_name_plural': 'Виджеты',
            },
        ),
    ]
