from aenum import IntEnum


class RespCode(IntEnum):
    # 正确的请求返回正确的结果
    OK = 200
    # 资源被正确的创建
    CREATED = 201
    # 已经接受请求，但是结果正在处理中
    ACCEPTED = 202
    # 资源删除成功
    NO_CONTENT = 204
    # 资源未修改,客户端可以使用缓存数据
    NOT_MODIFIED = 304
    # 请求的语法错误
    BAD_REQUEST = 400
    # 请求要求用户的身份认证
    Unauthorized = 401
    # 服务器理解请求客户端的请求,但是拒绝执行此请求
    FORBIDDEN = 403
    # 请求的资源不存在
    NOT_FOUND = 404
    # 请求频率过快
    TWO_MANY_REQUESTS = 429
    # 服务端错误
    INTERNAL_SERVER_ERROR = 500


class Constants(IntEnum):
    INIT_COINS = 10
    ORDER_BY_CREATED = 1
    ORDER_BY_IS_TOP = 2
    APP_MODEL_BLOG = 15
    APP_MODEL_COMMENT = 14
    # todo 部署需要修改


# todo 部署需要修改
VUE_HOST = 'http://localhost:8080/'
