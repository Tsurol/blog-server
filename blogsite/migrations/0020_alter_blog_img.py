# Generated by Django 3.2.7 on 2021-11-20 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogsite', '0019_alter_blog_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='img',
            field=models.FileField(blank=True, null=True, upload_to='blogCover', verbose_name='图片地址'),
        ),
    ]
