from lecture.models import Course, Takes
from users.models import User
from users.serializers import *
from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from lecture.views import CourseViewSet
from maps.views import ClassroomListView


def get_user_info(username):
    user = User.objects.filter(username=username)
    return UserSerializer(user, many=True).data


def get_course_info(semester="", name="", credit="", day="", classroom="", advisor="", major=""):
    queryset = Course.objects.all()

    if semester:
        queryset = queryset.filter(semester=semester)
    if name:
        queryset = queryset.filter(name__icontains=name)
    if credit:
        queryset = queryset.filter(credit=credit)
    if day:
        queryset = queryset.filter(day__icontains=day)
    if classroom:
        queryset = queryset.filter(classroom__icontains=classroom)
    if advisor:
        queryset = queryset.filter(advisor__icontains=advisor)
    if major:
        queryset = queryset.filter(major__icontains=major)

    print("CourseSerialser: ", CourseSerializer(queryset, many=True).data)
    return CourseSerializer(queryset, many=True).data


def get_takes_info(username, semester=""):
    takes = Takes.objects.filter(student_id=username)
    if semester:
        takes = takes.filter(semester=semester)
    print("Takes: ", takes)
    return TakesSerializer(takes, many=True).data  # To.윤상현  Modified Sererializer


def get_empty_classrooms(building):
    # Fetching classroom info
    empty_classrooms_data = ClassroomListView.get_classroom_info(building)
    print("EmptyClassrooms: ", empty_classrooms_data)
    
    # Ensure this is returning a tuple or list of two elements if that is what the serializer expects
    # For example:
    return empty_classrooms_data, []  # Assuming no occupied classrooms are returned



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

def main():
    # Demo 함수
    username = "20191559"
    semester = "2024010"
    course_id = "CSE4187"
    building = "K"
    
    # user_info = get_user_info(username)
    # print("User Info:", user_info)
    
    # course_info = get_course_info()
    # print("Course Info:", course_info)
    
    # filtered_course_info = get_course_info_by_filter(course_id=course_id, semester=semester)
    # print("Filtered Course Info:", filtered_course_info)
    
    # takes_info = get_takes_info(username, semester)
    # print("Takes Info:", takes_info)
    
    empty_classrooms = get_empty_classrooms(building)
    print("Empty Classrooms:", empty_classrooms)

if __name__ == "__main__":
    main()