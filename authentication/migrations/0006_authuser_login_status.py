# Generated by Django 3.2.7 on 2021-09-24 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_loginrecord_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuser',
            name='login_status',
            field=models.SmallIntegerField(choices=[(1, '未登录'), (0, '登录中')], default=1, verbose_name='登录状态'),
        ),
    ]
