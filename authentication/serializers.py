import string

from rest_framework import serializers
from authentication.models import AuthUser, UserProfile
from blog.serializers import CustomFieldsSerializer


class UserProfileSerializer(CustomFieldsSerializer):
    coins = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_coins(self, obj):
        """ 用户资产（鲨币） """
        return obj.user.asset.coins


class AuthUserSerializer(CustomFieldsSerializer):
    profile = UserProfileSerializer(fields=('id', 'nickname', 'avatar', 'sex', 'age', 'is_valid'))

    class Meta:
        model = AuthUser
        fields = '__all__'
