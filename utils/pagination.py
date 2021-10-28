# coding:utf-8

from rest_framework.pagination import LimitOffsetPagination


class MyPagination(LimitOffsetPagination):
    # 默认每页显示多少条数据,没有则从settings中找page_size
    default_limit = 10
    # 表示索引的位置,从0开始索引,默认使用offset为key
    offset_query_param = 'offset'
    # 表示每索引一页时,数据显示多少条
    limit_query_param = 'limit'
    # 显示数据时,最大多少条每一页，默认为None
    max_limit = 20
