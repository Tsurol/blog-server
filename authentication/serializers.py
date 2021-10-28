import string

from rest_framework import serializers
from authentication.models import AuthUser, UserProfile
from blog.serializers import CustomFieldsSerializer


class UserProfileSerializer(CustomFieldsSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class AuthUserSerializer(CustomFieldsSerializer):
    profile = UserProfileSerializer(fields=('id', 'nickname', 'avatar', 'sex', 'age', 'is_valid'))

    class Meta:
        model = AuthUser
        fields = '__all__'
