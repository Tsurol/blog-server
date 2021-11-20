from rest_framework import serializers
from utils.enums import VUE_HOST
from authentication.models import UserProfile
from authentication.serializers import UserProfileSerializer, AuthUserSerializer
from blog.serializers import CustomFieldsSerializer
from blogsite.models import Blog, Tag, Comment
from utils.filter import time_filter


class BlogSerializer(CustomFieldsSerializer):
    created_at = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    love_count = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'

    def get_img(self, obj):
        if obj.img:
            # todo：部署时需要更改
            return 'http://127.0.0.1:8000/media/' + str(obj.img)
        return None

    def get_created_at(self, obj):
        """ 博客发布时间格式化 """
        return obj.created_at.strftime('%Y-%m-%d')

    def get_user(self, obj):
        """ 获取作者的昵称 """
        if obj.user.profile.is_valid:
            return obj.user.profile.nickname
        return None

    def get_comment_count(self, obj):
        """ 获取博客下的评论数量 """
        return obj.blog_comment_list.filter(is_valid=True).count()

    def get_love_count(self, obj):
        """ 获取博客下的点赞数量 """
        return obj.love.filter(is_valid=True).count()


class TagSerializer(CustomFieldsSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class BlogDetailSerializer(CustomFieldsSerializer):
    created_at = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    love_count = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'

    def get_category(self, obj):
        """ 分类专栏 """
        return obj.category.name

    def get_created_at(self, obj):
        """ 博客发布时间格式化 """
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_user(self, obj):
        """ 获取作者的昵称 """
        if obj.user.profile.is_valid:
            return obj.user.profile.nickname
        return None

    def get_comment_count(self, obj):
        """ 获取博客下的评论数量 """
        return obj.blog_comment_list.filter(is_valid=True).count()

    def get_love_count(self, obj):
        """ 获取博客下的点赞数量 """
        return obj.love.filter(is_valid=True).count()


class BlogCommentSerializer(CustomFieldsSerializer):
    user = AuthUserSerializer(fields=('id', 'username', 'email', 'profile'))
    temporary_nickname = serializers.SerializerMethodField()
    temporary_avatar = serializers.SerializerMethodField()
    reply = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    love_count = serializers.SerializerMethodField()
    blog_title = serializers.SerializerMethodField()
    blog = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_blog(self, obj):
        return obj.blog.id

    def get_blog_title(self, obj):
        return obj.blog.title

    def get_love_count(self, obj):
        return obj.love.filter(is_valid=True).count()

    def get_created_at(self, obj):
        """ 博客发布时间格式化 """
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_created_at(self, obj):
        """ 博客发布时间格式化 """
        return time_filter(dt=obj.created_at)

    def get_temporary_nickname(self, obj):
        """ 获取临时用户的昵称 """
        if not obj.temporary:
            return None
        return obj.temporary

    def get_temporary_avatar(self, obj):
        """ 获取临时用户的临时头像 """
        if not obj.temporary:
            return None
        # todo 部署时需要更改
        return VUE_HOST + 'static/default_avatar.jpg'

    def get_reply(self, obj):
        # 获取评论下的回复
        reply_ls = Comment.objects.filter(reply_id=obj.id).all()
        reply_list = []
        for item in reply_ls:
            reply_list.append({
                'id': item.id,
                # todo 部署时需要更改
                'avatar': VUE_HOST + 'static/default_avatar.jpg' if item.temporary else item.user.profile.avatar,
                'nickname': item.temporary if item.temporary else item.user.profile.nickname,
                'content': item.content,
                'created_at': item.format_created_at
            })
        if len(reply_list) == 0:
            return None
        return reply_list
