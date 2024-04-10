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

class TakesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Takes
        fields = '__all__'
