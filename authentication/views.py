from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.bussiness import send_verify_code, register_by_email, login_by_username, reset_pwd_by_email, \
    get_user_info, update_user_info, login_by_email_code
from utils.enums import RespCode
from utils.response import reformat_resp
from utils.verify import current_user


class SendEmailCodeView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = 'verify_code'

    def post(self, request):
        try:
            email = request.data.get('email', None)
            code, resp = send_verify_code(email)
            if code == RespCode.CREATED.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')


class LoginByEmailCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email = request.data.get('email', None)
            code = request.data.get('code', None)
            code, resp = login_by_email_code(request, email, code)
            if code == RespCode.CREATED.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')


class EmailRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            username = request.data.get('username', None)
            email = request.data.get('email', None)
            verify_code = request.data.get('verify_code', None)
            password = request.data.get('password', None)
            code, resp = register_by_email(request, email, verify_code, password, username)
            if code == RespCode.CREATED.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')


class LoginByUsernameView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            username = request.data.get('username', None)
            password = request.data.get('password', None)
            code, resp = login_by_username(request, username, password)
            if code == RespCode.CREATED.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')


class ResetPasswordByEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            email = request.data.get('email', None)
            verify_code = request.data.get('verify_code', None)
            password = request.data.get('password', None)
            repeat = request.data.get('repeat', None)
            code, resp = reset_pwd_by_email(request, email, password, verify_code, repeat)
            if code == RespCode.CREATED.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            code, resp = get_user_info(request)
            if code == RespCode.OK.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')

    def put(self, request):
        try:
            nickname = request.data.get('nickname', None)
            avatar = request.data.get('avatar', None)
            sex = request.data.get('sex', None)
            age = request.data.get('age', None)
            code, resp = update_user_info(request, nickname, avatar, sex, age)
            if code == RespCode.CREATED.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')

