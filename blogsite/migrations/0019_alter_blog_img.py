# Generated by Django 3.2.7 on 2021-11-19 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogsite', '0018_blog_is_origin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='img',
            field=models.CharField(blank=True, default=None, max_length=256, null=True, verbose_name='图片地址'),
        ),
    ]
