from lecture.models import Course, Takes
from users.models import User
from users.serializers import *
def get_user_info(username):
    user = User.objects.filter(username=username)
    return UserSerializer(user, many=True).data

def get_course_info():
    course = Course.objects.all()
    return CourseSerializer(course, many=True).data

def get_takes_info(username):
    takes = Takes.objects.filter(student_id=username)
    return TakesSerializer(takes, many=True).data
    