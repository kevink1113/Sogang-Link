from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
from drf_yasg import openapi
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .crawl_saint import get_saint_cookies
from .auth_backend import PasswordlessAuthBackend
from django.contrib.auth import login as auth_login

from drf_yasg.utils import swagger_auto_schema


class LoginView(APIView):
    """
    post:
    사용자 로그인(회원가입)을 위한 엔드포인트

    username과 password를 JSON 형태로 전달받아 인증을 수행
    인증에 성공하면, 사용자 토큰을 반환

    요청 예시:
    {
        "username": "2019xxxx",
        "password": "password123"
    }

    응답 예시:
    {
        "token": "1234567890abcdef"
    }
    """

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='학번'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='비밀번호')
        }
        # response 정의

    ))
    # @swagger_auto_schema(operation_description="POST 요청을 위한 엔드포인트입니다.")
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        # print(username, password)
        cookies = get_saint_cookies(username, password)
        if cookies is None:
            return Response({'error': 'Invalid Credentials or Saint Cookies not retrieved'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = PasswordlessAuthBackend().authenticate(username=username, cookies=cookies)
        if user is None:
            return Response({'error': 'Authentication Failed'}, status=status.HTTP_404_NOT_FOUND)

        auth_login(request, user, backend='backend.auth_backend.PasswordlessAuthBackend')  # Django login

        # 토큰이 이미 존재하면 가져오고, 그렇지 않으면 생성합니다.
        token, created = Token.objects.get_or_create(user=user)
        print("Token: ", token.key, "Created: ", created)
        # 'created' 변수는 토큰이 새로 생성되었는지 여부를 나타냅니다.
        # 여기서 추가적인 로직을 구현할 수 있습니다 (예: 로그 생성).

        return Response({'token': token.key}, status=status.HTTP_200_OK)


def my_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cookies = get_saint_cookies(username, password)
        if cookies is None:
            return render(request, 'login.html')
        user = PasswordlessAuthBackend().authenticate(username=username, cookies=cookies)
        # login 함수 호출
        auth_login(request, user)
        return redirect('/')
    else:
        # GET 요청 처리
        pass
    return render(request, 'login.html')


def offline(request):
    return render(request, 'offline.html')
