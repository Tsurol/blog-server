# Generated by Django 3.2.7 on 2021-11-08 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogsite', '0009_blog_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='img',
            field=models.ImageField(blank=True, default=None, max_length=256, null=True, upload_to='blogImg/%Y%m', verbose_name='图片地址'),
        ),
    ]