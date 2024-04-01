# # from django.contrib.auth.models import User
# from users.models import User
#
# from django.contrib.auth.password_validation import validate_password  # Django의 기본 pw 검증 도구
#
# from rest_framework import serializers
# from rest_framework.authtoken.models import Token  # Token 모델
# from rest_framework.validators import UniqueValidator  # 이메일 중복 방지를 위한 검증 도구
#
#
# class RegisterSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(
#         validators=[UniqueValidator(queryset=User.objects.all())]  # 중복 방지
#     )
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])  # 비밀번호 검증
#
#     class Meta:
#         model = User
#         fields = ('email', 'username', 'password')
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }
#
#     def create(self, validated_data):
#         user = User.objects.create_user(validated_data['username'], validated_data['password'])
#
#         Token.objects.create(user=user)  # Token 생성
#
#         return user
