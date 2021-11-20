import string

from rest_framework import serializers
from authentication.models import AuthUser, UserProfile
from blog.serializers import CustomFieldsSerializer
from blogsite.models import Blog, Comment


class UserProfileSerializer(CustomFieldsSerializer):
    coins = serializers.SerializerMethodField(read_only=True)
    blog = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_avatar(self, obj):
        if obj.avatar:
            # todo 部署需修改
            return 'http://127.0.0.1:8000/media/' + str(obj.avatar)
        return None

    def get_coins(self, obj):
        """ 用户资产（鲨币） """
        return obj.user.asset.coins

    def get_blog(self, obj):
        user = obj.user
        blog_qs = Blog.objects.filter(is_valid=True, user=user).all()
        blog_count = blog_qs.count()
        comment_qs = Comment.objects.filter(is_valid=True, blog__in=blog_qs).all()
        comment_count = comment_qs.count()
        return {
            'blog_count': blog_count,
            'comment_count': comment_count
        }


class AuthUserSerializer(CustomFieldsSerializer):
    profile = UserProfileSerializer(fields=('id', 'nickname', 'avatar', 'sex', 'age', 'is_valid'))

    class Meta:
        model = AuthUser
        fields = '__all__'
