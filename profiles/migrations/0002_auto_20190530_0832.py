# Generated by Django 2.0.6 on 2019-05-30 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_birth',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
    ]