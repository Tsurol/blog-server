from rest_framework.response import Response


def reformat_resp(code, body, message=''):
    data = {
        'code': code,
        'body': body,
        'message': message
    }
    resp = Response(data, status=code)
    return resp


def error_resp(code, message=''):
    data = {
        "error_code": code,
        'error_msg': message
    }
    resp = Response(data)
    return resp
