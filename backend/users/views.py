# views.py in your users app

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from backend.auth_backend import PasswordlessAuthBackend
from .serializers import UserSerializer
from backend.crawl_saint import get_student_info

User = get_user_model()

class UpdateUserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            backend = PasswordlessAuthBackend()
            
            info = get_student_info(user.login_cookie)
            print("User info updated")
            backend.update_user_info(user, info, user.login_cookie) 
            
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
            backend.manage_all_takes(user, user.login_cookie)
            return Response({"message": "Takes updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateGradesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            backend = PasswordlessAuthBackend()
            backend.manage_all_grades(user, user.login_cookie)
            return Response({"message": "Grades updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
