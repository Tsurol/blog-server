from django.db import models
from mdeditor.fields import MDTextField

from authentication.models import AuthUser


class CommonModel(models.Model):
    is_valid = models.BooleanField('逻辑删除', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True


class Blog(CommonModel):
    title = models.CharField('标题', max_length=64)
    desc = models.CharField('简述', max_length=256)
    content = MDTextField()
    is_top = models.BooleanField('置顶', default=False)
    is_hot = models.BooleanField('热门博客', default=False)
    user = models.ForeignKey(verbose_name='关联用户', to=AuthUser, on_delete=models.CASCADE,
                             related_name='blog_list')

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = '博客'
        db_table = 'blog'
        ordering = ['id']

    def __str__(self):
        return self.title


class Comment(CommonModel):
    content = models.TextField('评论内容')
    is_top = models.BooleanField('置顶', default=False)
    love_count = models.IntegerField('点赞', default=0)
    reply = models.ForeignKey(verbose_name='评论的回复', to='self', blank=True, null=True,
                              related_name='comment_reply',
                              on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        db_table = 'blog_comment'

    def __str__(self):
        return self.id
