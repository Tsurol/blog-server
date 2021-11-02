from blogsite.models import Blog, Tag
from blogsite.serializers import BlogSerializer, TagSerializer
from utils.enums import RespCode
from utils.pagination import MyPagination


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
    fields = ('id', 'title', 'desc', 'created_at', 'bkc', 'user', 'is_top', 'comment_count')
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
