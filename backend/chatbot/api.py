from django.utils import timezone
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

from maps.models import Building, Facility, Menu, Restaurant
from .serializers import BuildingSerializer, FacilitySerializer, MenuSerializer, RestaurantSerializer


from maps.models import Building, Facility, Menu, Restaurant
from .serializers import BuildingSerializer, FacilitySerializer, MenuSerializer, RestaurantSerializer


from maps.models import Building, Facility, Menu, Restaurant
from .serializers import BuildingSerializer, FacilitySerializer, MenuSerializer, RestaurantSerializer


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


def get_takes_info(username, semester="", final_grade=""):
    print("[" + semester + " " + final_grade + "]")
    takes = Takes.objects.filter(student_id=username)
    if semester:
        takes = takes.filter(course__semester=semester)
    if final_grade:
        takes = takes.filter(final_grade__icontains=final_grade)
    print("Takes: ", takes)
    return TakesSerializer(takes, many=True).data  # To.윤상현  Modified Sererializer


def get_grade(grade):
    if ord(grade[0]) >= ord('F'):
        return 0.
    res = 4. + ord('A') - ord(grade[0])
    if grade[1] == '+':
        res += 0.3
    elif grade[1] == '-':
        res -= 0.3
    return res


def get_average_grade(username, semester=""):
    takes = Takes.objects.filter(student=username, course__semester__icontains=semester)
    print(takes)
    res = 0.
    credit = 0.
    for subject in takes:
        print(subject.final_grade,end="")
        res += get_grade(subject.final_grade)*subject.course.credit
        if subject.final_grade[0] <= 'F':
            credit += subject.course.credit
    print("\n"+str(res)+"/"+str(credit))
    return res/credit if credit != 0. else 0




def get_empty_classrooms(building):
    # Fetching classroom info
    empty_classrooms_data = ClassroomListView.get_classroom_info(building)
    print("EmptyClassrooms: ", empty_classrooms_data)

    # Ensure this is returning a tuple or list of two elements if that is what the serializer expects
    # For example:
    return empty_classrooms_data, []  # Assuming no occupied classrooms are returned


def get_current_info(username):
    def get_current_date():
        return timezone.now().strftime('%Y-%m-%d %H:%M:%S')

    def get_current_semester():
        month = timezone.now().month
        semester = ''
        if 3 <= month <= 6:
            semester = '1학기 (봄학기)'
        elif 7 <= month <= 8:
            semester = '여름학기'
        elif 9 <= month <= 12:
            semester = '2학기 (가을학기)'
        else:
            semester = '겨울학기'

        year = timezone.now().year
        if 1 <= month <= 2:
            return f'{year-1}-{semester}'
        else:
            return f'{year}-{semester}'

    def get_academic_progress(username):
        user = User.objects.filter(username=username).first()
        if not user:
            return 'User not found'

        current_year = user.year
        current_semester = user.semester

        return f'{current_year}학년 {current_semester}학기생'

    return {
        'current_date': get_current_date(),
        'current_semester': get_current_semester(),
        'academic_progress': get_academic_progress(username)
    }


def get_building_info(building_name):
    try:
        print("Trying to get ", building_name)
        building = Building.objects.get(name=building_name)
        building_data = BuildingSerializer(building).data
        print("Building data: ", building_data)
        return {
            'status': 'success',
            'building_data': building_data
        }
    except Building.DoesNotExist:
        return {
            'status': 'error',
            'message': f'Building "{building_name}" not found.'
        }
    
def get_facility_info(facility_name):
    try:
        facility = Facility.objects.get(name=facility_name)
        facility_data = FacilitySerializer(facility).data
        return {
            'status': 'success',
            'facility_data': facility_data
        }
    except Facility.DoesNotExist:
        return {
            'status': 'error',
            'message': f'Facility "{facility_name}" not found.'
        }

def get_menu_info(facility_name, date):
    try:
        menu = Menu.objects.get(facility__name=facility_name, date=date)
        menu_data = MenuSerializer(menu).data
        return {
            'status': 'success',
            'menu_data': menu_data
        }
    except Menu.DoesNotExist:
        return {
            'status': 'error',
            'message': f'Menu for facility "{facility_name}" on date "{date}" not found.'
        }


def get_filtered_restaurants(name=None, category=None, place=None, min_price=None, max_price=None, tag=None):
    print("====== Get Filtered Restaurants =======")
    print("Name: ", name, "Category: ", category, "Place: ", place, "Min Price: ", min_price, "Max Price: ", max_price, "Tag: ", tag)
    restaurants = Restaurant.objects.all()

    if name:
        restaurants = restaurants.filter(name__icontains=name)
    if category:
        restaurants = restaurants.filter(category__icontains=category)
    if place:
        restaurants = restaurants.filter(place__icontains=place)
    if min_price is not None:
        restaurants = restaurants.filter(avg_Price__gte=min_price)
    if max_price is not None:
        restaurants = restaurants.filter(avg_Price__lte=max_price)
    if tag:
        restaurants = restaurants.filter(tags__name__icontains=tag)

    restaurant_data = RestaurantSerializer(restaurants, many=True).data
    return {
        'status': 'success',
        'restaurant_data': restaurant_data
    }


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