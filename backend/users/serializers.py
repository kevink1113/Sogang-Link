# serializers.py in your users app

from rest_framework import serializers
from django.contrib.auth import get_user_model
from lecture.models import Course, Takes

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'name', 'year', 'semester', 'advisor', 'major')

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

# class TakesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Takes
#         fields = '__all__'


class TakesSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Takes
        fields = ['course', 'middle_grade', 'final_grade']

# class FreeClassroomSerializer(serializers.Serializer):
#     classroom = serializers.CharField(max_length=100)
#     free_until = serializers.CharField(max_length=100)

# class AvailableClassroomSerializer(serializers.Serializer):
#     classroom = serializers.CharField(max_length=100)
#     available_from = serializers.CharField(max_length=100)

class EmptyClassroomSerializer(serializers.Serializer):
    def to_representation(self, instance):
        free_classrooms, occupied_classrooms = instance
        data = {
            'free': [classroom['classroom'] for classroom in free_classrooms],
            'occupied': [classroom['classroom'] for classroom in occupied_classrooms if 'available_from' in classroom]
        }
        return data