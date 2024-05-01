from lecture.models import Course, Takes
from users.models import User
from users.serializers import *
from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from lecture.views import CourseViewSet

def get_user_info(username):
    user = User.objects.filter(username=username)
    return UserSerializer(user, many=True).data

def get_course_info():
    course = Course.objects.all()
    print("CourseSerialser: ", CourseSerializer(course, many=True).data)
    return CourseSerializer(course, many=True).data


def get_takes_info(username):
    takes = Takes.objects.filter(student_id=username)
    return TakesSerializer(takes, many=True).data # To.윤상현  Modified Sererializer
    

# API 재활용 방안 강구 중
# def get_takes_info(user):
#     # Assuming that 'user' is an instance of your User model or an ID that can identify the user
    
#     # Use APIClient for better integration with DRF features
#     client = APIClient()

#     # Simulate user authentication if necessary
#     client.force_authenticate(user=user)

#     # Construct the URL for the takes listing endpoint
#     # url = reverse('takes-list')  # Ensure you have named your URL in urls.py
#     url = '/lecture/takes'  # Assuming the URL is '/takes/'

#     # Optional: Include any query parameters if needed
#     params = {
#         'semester': '2024010',
#         # 'day': '2',
#         # 'credit': '3',
#         # 'name': 'Biology',
#         # 'major': 'Biosciences',
#         # 'real': 'true'
#     }

#     # Perform the GET request
#     response = client.get(url, params)
#     print("RESPONSE: ", response.data)

#     # Check if the response is successful
#     if response.status_code == status.HTTP_200_OK:
#         return response.data  # Directly use the DRF response data
#     else:
#         return {'error': 'Data not found', 'status': response.status_code}
    
# A simple internal API client
# def internal_api_client(url, params):
#     factory = APIRequestFactory()
#     request = factory.get(url, params, format='json')
#     view = CourseViewSet.as_view({'get': 'list'})
#     response = view(request)
#     return response.data

# # Usage
# def get_takes_info(user):
#     data = internal_api_client('/lecture/takes', {'semester': '2024010'})
#     return data