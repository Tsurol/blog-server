from rest_framework import serializers

from blog.serializers import CustomFieldsSerializer
from blogsite.models import Blog, Tag


class BlogSerializer(CustomFieldsSerializer):
    created_at = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'

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


class TagSerializer(CustomFieldsSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
