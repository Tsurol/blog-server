# Generated by Django 3.2.7 on 2021-09-27 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_userprofile_is_valid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authuser',
            name='login_status',
            field=models.SmallIntegerField(choices=[(0, '登陆中'), (1, '未登录')], default=1, verbose_name='登录状态'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='sex',
            field=models.SmallIntegerField(choices=[(11, '男'), (12, '女')], default=11, verbose_name='性别'),
        ),
    ]
