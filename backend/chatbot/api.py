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


'''
    course_id = models.CharField(max_length=10, null=True)
    semester = models.IntegerField()
    name = models.CharField(max_length=30, null=True)
    credit = models.IntegerField(null=True)  # 학점
    day = models.IntegerField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    classroom = models.CharField(max_length=15, default='', null=True)
    advisor = models.CharField(max_length=30, null=True)
    major = models.CharField(max_length=30, null=True)
'''


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


def get_course_info_by_filter(
        course_id="", semester="", name="", credit="", day="", classroom="", advisor="", major=""):
    # 일단 각 항 혹은 역할마다 api를 따로 만드는 것이 좋은지?
    # 아니면 이렇게 통합해서 하나로 만든 다음에 인수를 받는 것에 대해서만 검색을 하게 하는게 좋은지?
    # 역할마다 따로 만들면, openai한테 함수 알려주는 부분이 엄청 길어져서 일단 이렇게만 해봄.
    # 혹시 함수를 if문으로 하드코딩 하는 거 말고 더 효율적인 방법이 있는지는 잘...

    # 그리고, openai에 알려주는 함수들의 목록과 실제 호출하는 함수들을 일치시킬 필요가 없다는 것도 생각해봐야함
    # 만약 openai가 여러 역할을 수행하는 함수를 잘 쓰지 못할 수도 있는데 (적절한 인수를 잘 못 준다던가)
    # 이 경우에는 알려 주는 함수는 세분화해놓고, 함수 이름 받아서 처리해주면 ok

    course = Course.objects.filter(
        course_id__contains=course_id,
        semester__contains=semester,
        name__contains=name,
        credit__contains=credit,
        day__contains=day,
        classroom__contains=classroom,
        advisor__contains=advisor,
        major__contains=major
    ).all()
    return CourseSerializer(course, many=True).data


'''
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='takes')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)  # TODO: 모든 학기를 크롤링 했다 가정할 때 null=False
    middle_grade = models.CharField(null=True, max_length=4)
    final_grade = models.CharField(null=True, max_length=4)
    real = models.BooleanField()
'''


def get_takes_info(username, semester):
    takes = Takes.objects.filter(student_id=username, course__semester=semester)
    print("Takes: ", takes)
    return TakesSerializer(takes, many=True).data  # To.윤상현  Modified Sererializer


def get_takes_info_by_filter(
        username, course="", middle_grade="", final_grade="", real="",
        semester="", name="", credit="", day="", classroom="", advisor="", major=""):
    # openai가 데이터를 쓸 때에, takes 전체랑 course 전체를 주어도 두 데이터 항목들을 잘 연결하지 못함.
    # 각 fk로 user랑 course를 참조하는 것을 api단에서 대신 해준다음에 데이터를 반환해야 할 듯함.
    # 그래서 takes를 filter로 받아오고, 각 takes에 대해 course랑 user를 참조해서 붙여가지고 줘야 할듯.
    # 어떻게 할지 논의가 필요할듯~
    # 그리고 내가 들은 과목 중에 3학점짜리를 찾아줘~ 같은 질문이 들어올 경우도 생각해보면
    # 애초에 처음부터 course랑 takes를 먼저 join한 다음에 filter를 해줘야 할 것 같기도 하고.

    takes_detail = Takes.objects.select_related('course').filter(course__course_id=course)

    takes = Takes.objects.filter(
        student_id=username,
        course_id=course,
        middle_grade=middle_grade,
        final_grade=final_grade,
        real=real
    ).all()
    return TakesSerializer(takes, many=True).data

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