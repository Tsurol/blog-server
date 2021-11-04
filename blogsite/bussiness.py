from django.db import transaction

from blogsite.models import Blog, Tag, Love
from blogsite.serializers import BlogSerializer, TagSerializer
from utils.enums import RespCode
from utils.pagination import MyPagination
from utils.verify import current_user


def get_blog_list(request, is_hot, is_top):
    bolg_qs = Blog.objects.filter(is_valid=True).all()
    if is_hot:
        bolg_qs = Blog.objects.filter(is_valid=True, is_hot=True).order_by('-updated_at').all()
    if is_top:
        bolg_qs = Blog.objects.filter(is_valid=True, is_top=True).order_by('-updated_at').all()
    if not bolg_qs:
        return RespCode.BAD_REQUEST.value, '查找的博客不存在'
    page_obj = MyPagination()
    page_res = page_obj.paginate_queryset(queryset=bolg_qs, request=request)
    fields = ('id', 'title', 'desc', 'created_at', 'bkc', 'user', 'comment_count', 'love_count')
    resp = {
        'data': BlogSerializer(page_res, many=True, fields=fields).data
    }
    return RespCode.OK.value, resp


def get_tag_list():
    tag_qs = Tag.objects.filter(is_valid=True).all()
    if not tag_qs:
        return RespCode.BAD_REQUEST.value, '查找的标签不存在'
    fields = ('id', 'name', 'bkc', 'blog')
    resp = {
        'data': TagSerializer(tag_qs, many=True, fields=fields).data
    }
    return RespCode.OK.value, resp


def love_blog(request, blog_id):
    user = current_user(request)
    if not user:
        return RespCode.BAD_REQUEST.value, '该账号不存在'
    blog_qs = Blog.objects.filter(id=blog_id, is_valid=True).first()
    if not blog_qs:
        return RespCode.BAD_REQUEST.value, '该博客不存在'
    love_qs = Love.objects.filter(user=user, blog=blog_qs).first()
    if love_qs:
        if love_qs.is_valid is True:
            love_qs.is_valid = False
            love_qs.save()
            return RespCode.CREATED.value, {}
        love_qs.is_valid = True
        love_qs.save()
        return RespCode.CREATED.value, {}
    Love.objects.create(user=user, blog=blog_qs)
    return RespCode.CREATED.value, {}
