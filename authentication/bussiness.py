import json
import re
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from authentication.models import AuthUser, LoginRecord
from authentication.serializers import AuthUserSerializer, UserProfileSerializer
from authentication.token import get_token_for_user
from utils.email_service import send_email
from utils.enums import RespCode
from utils.id import id_generator
from utils.verify import current_user


def save_user(request, user):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        user_ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        user_ip = request.META['REMOTE_ADDR']
    with transaction.atomic():
        # user.login_status = LoginStatusType.LOGGING
        LoginRecord.objects.create(username=user.username, ip=user_ip, user=user)
        user.last_login = timezone.now()
        user.save()
    refresh_dict = get_token_for_user(user)
    username = AuthUserSerializer(user, fields=('username',)).data.get('username')
    email = AuthUserSerializer(user, fields=('email',)).data.get('email')
    resp = {
        'username': username,
        'email': email,
        'access': refresh_dict.get('access', ''),
        'refresh': refresh_dict.get('refresh', '')
    }
    return resp


def send_verify_code(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return RespCode.BAD_REQUEST.value, "Email地址不合法"
    key = 'verify_code_email:{}'.format(email)
    verify_code = id_generator(5)
    if not settings.DEBUG:
        res = send_email(email, verify_code)
        if res == status.HTTP_201_CREATED:
            cache.set(key, json.dumps(verify_code), 60 * 2)
            return RespCode.CREATED.value, {}
        return RespCode.INTERNAL_SERVER_ERROR.value, '发送邮件失败，请稍后再试'
    else:
        cache.set(key, json.dumps(verify_code), 60)
        return RespCode.CREATED.value, {'verify_code': verify_code}


def login_by_email_code(request, email, code):
    user = AuthUser.objects.filter(email=email).first()
    code = code.upper()
    key = 'verify_code_email:{}'.format(email)
    cache_code = cache.get(key)
    if cache_code and json.loads(cache_code) == code:
        if user:
            cache.delete(key)
            refresh_dict = get_token_for_user(user)
            username = AuthUserSerializer(user, fields=('username',)).data.get('username')
            email = AuthUserSerializer(user, fields=('email',)).data.get('email')
            resp = {
                'username': username,
                'email': email,
                'access': refresh_dict.get('access', ''),
                'refresh': refresh_dict.get('refresh', '')
            }
            return RespCode.CREATED.value, resp
        # 如果查不到这个用户，则创建一个用户
        # 匿名用户的默认密码是anonymous todo：默认密码应该随机生成!
        user = AuthUser.objects.create_anonymous_user(username=email, password='anonymous', email=email)
        resp = save_user(request, user)
        return RespCode.CREATED.value, resp

    return RespCode.BAD_REQUEST.value, '邮箱或验证码有误'


def register_by_email(request, email, verify_code, password):
    if not email or not verify_code or not password:
        return RespCode.BAD_REQUEST.value, '请求参数错误'
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return RespCode.BAD_REQUEST.value, "Email地址不合法"
    if len(password) > 17:
        return RespCode.BAD_REQUEST.value, '密码过长'
    if len(password) < 4:
        return RespCode.BAD_REQUEST.value, '密码过短'
    is_email_exists = AuthUser.objects.filter(email=email).first()
    if is_email_exists:
        return RespCode.BAD_REQUEST.value, '邮箱已存在'
    verify_code = verify_code.upper()
    key = 'verify_code_email:{}'.format(email)
    cache_code = cache.get(key)
    if cache_code and json.loads(cache_code) == verify_code:
        cache.delete(key)
        # 用户名默认为注册时的邮箱
        user = AuthUser.objects.create_user(username=email, email=email, password=password)
        resp = save_user(request, user)
        return RespCode.CREATED.value, resp
    return RespCode.BAD_REQUEST.value, '验证码错误'


def login_by_email(request, email, password):
    user = AuthUser.objects.filter(username=email).first()
    if not user:
        return RespCode.NOT_FOUND.value, '该账号不存在'
    # if user.login_status == LoginStatusType.LOGGING:
    #     return RespCode.BAD_REQUEST.value, '该账号已登录，请不要重复操作'
    verify = check_password(password, user.password)
    if verify:
        resp = save_user(request, user)
        return RespCode.CREATED.value, resp
    return RespCode.BAD_REQUEST.value, '账号或密码错误'


def reset_pwd_by_email(request, email, password, verify_code, repeat):
    user = current_user(request)
    if not user:
        return RespCode.BAD_REQUEST.value, '该账号不存在'
    code = verify_code.upper()
    key = 'verify_code_email:{}'.format(email)
    cache_code = cache.get(key)
    if cache_code and json.loads(cache_code) == code:
        cache.delete(key)
        if password != repeat:
            return RespCode.BAD_REQUEST.value, '两次输入密码不一致'
        new_password = make_password(password)
        user.password = new_password
        user.save()
        # 修改密码后会自动退出登录!
        return RespCode.CREATED.value, {}
    return RespCode.BAD_REQUEST.value, '验证码错误'


def get_user_info(request):
    user = current_user(request)
    if not user:
        return RespCode.BAD_REQUEST.value, '该账号不存在'
    if not user.profile.is_valid:
        return RespCode.BAD_REQUEST.value, '用户个人信息已被删除'
    fields = ('user', 'username', 'nickname', 'avatar', 'sex', 'age')
    user_profile_data = UserProfileSerializer(user.profile, fields=fields).data
    return RespCode.OK.value, user_profile_data


def update_user_info(request, nickname, avatar, sex, age):
    user = current_user(request)
    if not user:
        return RespCode.BAD_REQUEST.value, '该账号不存在'
    if not any([nickname, avatar, sex, age]):
        return RespCode.BAD_REQUEST.value, '未传入需要修改的信息'
    if not user.profile.is_valid:
        return RespCode.BAD_REQUEST.value, '用户个人信息已被删除'
    if nickname:
        user.profile.nickname = nickname
        user.profile.updated_at = timezone.now()
        user.profile.save()
    if avatar:
        user.profile.avatar = avatar
        user.profile.updated_at = timezone.now()
        user.profile.save()
    if sex:
        user.profile.sex = sex
        user.profile.updated_at = timezone.now()
        user.profile.save()
    if age:
        user.profile.age = age
        user.profile.updated_at = timezone.now()
        user.profile.save()
    return RespCode.CREATED.value, {}

