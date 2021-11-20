from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from mdeditor.fields import MDTextField

from authentication.models import AuthUser
from utils.enums import VUE_HOST
from utils.filter import time_filter


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
    # VUE_HOST + 'static/xxx.jpg'
    # img = models.CharField('图片地址', max_length=256, null=True, blank=True, default=None)
    img = models.ImageField('图片地址', max_length=300, null=True, blank=True, upload_to='cover/%Y/%m/%d', default=None)
    is_origin = models.BooleanField('是否原创', default=True)
    user = models.ForeignKey(verbose_name='关联用户', to=AuthUser, on_delete=models.CASCADE,
                             related_name='blog_list')
    love = GenericRelation(to='LoveRelated', verbose_name='关联点赞表')
    category = models.ForeignKey(verbose_name='关联分类专栏', to='Category', on_delete=models.SET_NULL, null=True,
                                 related_name='category_blog_list')

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

    @property
    def format_created_at(self):
        return time_filter(dt=self.created_at)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        db_table = 'blog_comment'


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


class AdviceUpload(models.Model):
    """ 需求提交 """
    name = models.CharField('姓名', max_length=64)
    mobile = models.CharField('联系方式', max_length=32)
    advice = models.CharField('建议', max_length=4096)
    remarks = models.CharField("备注信息", max_length=8192, null=True, blank=True, default=None)
    create_time = models.DateTimeField("创建时间", editable=False, auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = '反馈建议'
        verbose_name_plural = '反馈建议'

    def __str__(self):
        return str(self.id)


class Category(models.Model):
    """ 分类专栏 """
    name = models.CharField('专栏名', max_length=64)
    remarks = models.CharField("备注信息", max_length=8192, null=True, blank=True, default=None)
    create_time = models.DateTimeField("创建时间", editable=False, auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = '分类专栏'
        verbose_name_plural = '分类专栏'

    def __str__(self):
        return self.name
