from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
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
    bkc = models.CharField('背景颜色', max_length=32, null=True, default='#adb5bd', blank=True)
    img = models.ImageField('图片地址', max_length=256, upload_to='blogImg/%Y%m', null=True, blank=True, default=None)
    user = models.ForeignKey(verbose_name='关联用户', to=AuthUser, on_delete=models.CASCADE,
                             related_name='blog_list')
    love = GenericRelation(to='LoveRelated', verbose_name='关联点赞表')

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = '博客'
        db_table = 'blog'
        ordering = ['id']

    def __str__(self):
        return str(self.title)


class Comment(CommonModel):
    content = models.TextField('评论内容')
    is_top = models.BooleanField('置顶', default=False)
    reply = models.ForeignKey(verbose_name='评论的回复', to='self', blank=True, null=True,
                              related_name='comment_reply',
                              on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='关联用户', to=AuthUser, on_delete=models.CASCADE,
                             related_name='user_comment_list', null=True, blank=True)
    temporary = models.CharField('临时用户名', max_length=32, null=True, blank=True)
    blog = models.ForeignKey(verbose_name='关联博客', to=Blog, on_delete=models.CASCADE,
                             related_name='blog_comment_list')
    love = GenericRelation(to='LoveRelated', verbose_name='关联点赞表')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        db_table = 'blog_comment'

    def __str__(self):
        return str(self.id)


class Tag(CommonModel):
    name = models.CharField('标签名称', max_length=32)
    bkc = models.CharField('背景色', max_length=32, default='#7fd5ea')
    blog = models.ManyToManyField(verbose_name='关联博客', to=Blog,
                                  related_name='blog_tag_list')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
        db_table = 'blog_Tag'

    def __str__(self):
        return str(self.name)


class LoveRelated(models.Model):
    user = models.ForeignKey(verbose_name='关联用户', to=AuthUser, on_delete=models.CASCADE,
                             related_name='user_love_list')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='关联的模型')
    object_id = models.PositiveIntegerField('具体对象id')
    content_object = GenericForeignKey('content_type', 'object_id')

    is_valid = models.BooleanField('逻辑删除', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = '点赞'
        db_table = 'Love_related'

    def __str__(self):
        return str(self.id)
