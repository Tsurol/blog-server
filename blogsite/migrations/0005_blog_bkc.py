# Generated by Django 3.2.7 on 2021-10-29 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogsite', '0004_auto_20211029_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='bkc',
            field=models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='背景颜色'),
        ),
    ]
