# views.py in your users app

import json

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from backend.auth_backend import PasswordlessAuthBackend
from .serializers import UserSerializer
from backend.crawl_saint import get_student_info

from drf_yasg.utils import swagger_auto_schema

User = get_user_model()

class UpdateUserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            backend = PasswordlessAuthBackend()

            cookies = json.loads(user.login_cookie)
            cookie_jar = requests.utils.cookiejar_from_dict(cookies)
            info = get_student_info(cookie_jar)
            backend.update_user_info(user, info, cookie_jar) 
            
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateTakesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            backend = PasswordlessAuthBackend()
            print("Updating takes")
            cookies = json.loads(user.login_cookie)
            cookie_jar = requests.utils.cookiejar_from_dict(cookies)
            backend.manage_all_takes(user, cookie_jar)
            return Response({"message": "Takes updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateGradesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            backend = PasswordlessAuthBackend()
            cookies = json.loads(user.login_cookie)
            cookie_jar = requests.utils.cookiejar_from_dict(cookies)
            backend.manage_all_grades(user, cookie_jar)
            return Response({"message": "Grades updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserInfoView(APIView):
    """
    get:
    현재 로그인한 사용자의 정보를 조회합니다.

    """

    @swagger_auto_schema(operation_description="GET 요청을 위한 엔드포인트")
    def get(self, request):
        user = request.user
        print(user.username, user.name, user.state, user.year, user.semester, user.major, user.advisor, user.nickname)

        try:
            return Response({
                        'username': user.username,  # 학번
                        'name': user.name,          # 이름
                        'state': user.state,        # 0: 재학, 1: 휴학, 2: 졸업
                        'year': user.year,          # 학년
                        'semester': user.semester,  # 학기
                        'major': user.major,        # 전공
                        'advisor': user.advisor,    # 지도교수
                        'nickname': user.nickname,  # 닉네임
                        }, 
                          status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)