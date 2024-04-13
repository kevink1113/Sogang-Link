from rest_framework import serializers
from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'  # 모든 필드를 포함하도록 설정
