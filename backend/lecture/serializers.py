from rest_framework import serializers
from .models import Course, Takes


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'  # 모든 필드를 포함하도록 설정


class TakesSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Takes
        fields = ['course', 'middle_grade', 'final_grade', 'real']
