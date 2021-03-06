# Generated by Django 3.2.7 on 2021-10-25 17:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=True, verbose_name='逻辑删除')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('is_top', models.BooleanField(default=False, verbose_name='置顶')),
                ('love_count', models.IntegerField(default=0, verbose_name='点赞')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_reply', to='blogsite.comment', verbose_name='评论的回复')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
                'db_table': 'blog_comment',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=True, verbose_name='逻辑删除')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('title', models.CharField(max_length=64, verbose_name='标题')),
                ('desc', models.CharField(max_length=256, verbose_name='简述')),
                ('content', mdeditor.fields.MDTextField()),
                ('is_top', models.BooleanField(default=False, verbose_name='置顶')),
                ('is_hot', models.BooleanField(default=False, verbose_name='热门博客')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_list', to=settings.AUTH_USER_MODEL, verbose_name='关联用户')),
            ],
            options={
                'verbose_name': '博客',
                'verbose_name_plural': '博客',
                'db_table': 'blog',
                'ordering': ['id'],
            },
        ),
    ]
