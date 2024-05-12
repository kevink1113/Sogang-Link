from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from lecture.models import Course
import datetime
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from maps.models import Building, Facility, Menu
from .serializers import MenuSerializer
from django_filters import rest_framework as filters


# Create your views here.


class BuildingInfo:
  def __init__(self, name, classrooms):
    self.name = name
    # self.classrooms = classrooms
    # facility info
    self.facility = {
      "toilet": "있음",
      "elevator": "없음",
      "parking": "없음",
      "vending_machine": "있음",
      "AED": "없음",
      "건물개방시간": "09:00 - 18:00",
      "열람실": False,
    }


buildings = [
      BuildingInfo("정문", []),
      BuildingInfo("알바트로스 탑", []),
      BuildingInfo("본관", []),
      BuildingInfo("게페르트남덕우경제관(GN관)", []),
      BuildingInfo("예수회공동체", []),
      BuildingInfo("삼성가브리엘관(GA관)", []),
      BuildingInfo("금호아시아나바오로경영관(GA관)", []),
      BuildingInfo("토마스모어관(T관)", []),
      BuildingInfo("마태오관(MA관)", []),
      BuildingInfo("메리홀(M관)", []),
      BuildingInfo("성이냐시오관(I관)", []),
      BuildingInfo("엠마오관(E관)", []),
      BuildingInfo("로욜라도서관", []),
      BuildingInfo("최양업관(CY관)", []),
      BuildingInfo("하비에르관(X관)", []),
      BuildingInfo("다산관(D관)", []),
      BuildingInfo("곤자가국제학사(GH)", []),
      BuildingInfo("후문", []),
      BuildingInfo("곤자가플라자(GP)", []),
      BuildingInfo("떼이야르관(TE관)", []),
      BuildingInfo("정하상관(J관)", []),
      BuildingInfo("포스코 프란치스코관(F관)", []),
      BuildingInfo("리치별관(RA관)", []),
      BuildingInfo("대운동장", []),
      BuildingInfo("아담샬관(AS관)", []),
      BuildingInfo("리치과학관(R관)", []),
      BuildingInfo("예수회센터", []),
      BuildingInfo("김대건관(K관)", []),
      BuildingInfo("벨라르미노학사", []),
      BuildingInfo("서강빌딩", []),
      BuildingInfo("남문", []),
      BuildingInfo("아루페관(AR관)", []),
      BuildingInfo("체욱관", []),
      BuildingInfo("청년광장", []),
      BuildingInfo("베르크만스 우정원(BW관)", []),
    ]


class ClassroomListView(APIView):
    @staticmethod
    def get_classroom_info(building):
        current_time = datetime.datetime.now()
        day = current_time.weekday() + 1  # Monday is 1, Sunday is 7

        # Define a regex pattern that matches the building followed by numbers
        if building == "D":
            regex_pattern = r"^\[D(B)?\d+\]$"  # Matches "[D123]", "[DB123]" but not "[DAB123]"
        else:
            regex_pattern = f"^\[{building}\d+\]$" if building else ".*"  # Standard regex for other buildings

        # 정규표현식에 맞춰 강의실을 필터링
        all_classrooms = set(Course.objects.filter(classroom__regex=regex_pattern).values_list('classroom', flat=True).distinct())
        today_classes = Course.objects.filter(day__icontains=day, semester=2024010, classroom__regex=regex_pattern).order_by('start_time', 'end_time')

        # for i in today_classes:
        #     print(i.course_id, i.classroom, i.start_time, i.end_time)
        # Track the latest end time for ongoing or past classes and next start time for future classes
        last_end_time = {}
        next_start_time = {}

        for course in today_classes:
            room = course.classroom
            if room in ["", None]:
                continue  # Skip empty or undefined room entries
            
            if course.start_time <= current_time.time() <= course.end_time:
                # Update last end time if the class is ongoing
                last_end_time[room] = course.end_time
            elif current_time.time() < course.start_time:
                # Update the next start time if the class is in the future
                if room not in next_start_time or next_start_time[room] > course.start_time:
                    next_start_time[room] = course.start_time

        free_classrooms = []
        occupied_classrooms = []

        for room in all_classrooms:
            if room in ["", None]:
                continue

            if room in last_end_time:
                if room in next_start_time:
                    # Calculate the break duration
                    break_duration = (datetime.datetime.combine(datetime.date.today(), next_start_time[room]) - 
                                      datetime.datetime.combine(datetime.date.today(), last_end_time[room])).total_seconds() / 60
                    if break_duration > 15:
                        # If the break is longer than 15 minutes, mark as soon available
                        availability = last_end_time[room].strftime('%H시 %M분') + "부터 사용 가능"
                        occupied_classrooms.append({'classroom': room, 'available_from': availability})
                else:
                    # No more classes today, so it's available after the last one ends
                    availability = last_end_time[room].strftime('%H시 %M분') + "부터 사용 가능"
                    occupied_classrooms.append({'classroom': room, 'available_from': availability})
            else:
                # If the room is not in last_end_time, it's currently free
                if room in next_start_time:
                    availability = next_start_time[room].strftime('%H시 %M분') + "까지 사용 가능"
                else:
                    availability = "오늘 남은 수업 없음"
                free_classrooms.append({'classroom': room, 'free_until': availability})
        return free_classrooms, occupied_classrooms
        # return ({
        #     "free_classrooms": free_classrooms,
        #     "occupied_classrooms": occupied_classrooms
        # })

    def get(self, request, format=None):
        free_classrooms, occupied_classrooms = self.get_classroom_info(request.GET.get('building'))
        test = self.get_classroom_info(request.GET.get('building'))
        print("TEST: ", test)
        return JsonResponse({
            "free_classrooms": free_classrooms, 
            "occupied_classrooms": occupied_classrooms
            }, status=200)


class BuildingInfoListView(APIView):
    
    def get(self, request, format=None):

        building = request.GET.get('building') # 약어로 받아옴


        empty_classrooms = ClassroomListView().get_classroom_info(building)[0] # ex. 'K'의 빈 강의실 정보
        # empty_classroom 배열로 변환
        empty_classrooms = [
            f"{room['classroom']}: {room['free_until']}" for room in empty_classrooms
        ]


        # Build the response object
        response_data = {
            # "readingRoom": [
            #     f"총 {total_seats}석",
            #     f"가용 {available_seats}석"
            # ],
            # "printShop": [
            #     "오픈" if is_open else "닫힘",
            #     f"시간: {hours}"
            # ],
            "emptyClassrooms": empty_classrooms
        }

        # if building is K or J append readingRoom to response data
        # if building in ["K", "J"]:
        #     build = Building.objects.get(abbr=building)
        #     facility = Facility.objects.get(building=build, facility_type='reading_room')
        #     response_data["readingRoom"] = [
        #         f"총 {facility.total_seats}석",
        #         f"가용 {facility.available_seats}석",
        #         f"열람실 시간: {facility.open_hours}"
        #     ]
        
        building = Building.objects.get(abbr=building)
        facilities = Facility.objects.filter(building=building)

        for facility in facilities:
            if facility.facility_type == 'reading_room':
                response_data["readingRoom"] = [
                    f"{facility.description}",
                    f"총 {facility.total_seats}석",
                    f"가용 {facility.available_seats}석",
                    f"열람실 시간: {facility.open_hours}"
                ]
            elif facility.facility_type == 'print_shop':
                response_data["printShop"] = [
                    f"{facility.description}",
                    f"시간: {facility.open_hours}"
                ]
            else:
                response_data["etc"] = [
                    f"{facility.description}",
                    f"시간: {facility.open_hours}"
                ]

        return JsonResponse(response_data, status=200)


class MenuFilter(filters.FilterSet):
    facility_name = filters.CharFilter(field_name='facility__name', lookup_expr='icontains')

    class Meta:
        model = Menu
        fields = ['facility_name', 'date']  # Specify all fields needed for filtering here


class MenuListView(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MenuFilter  # Use this to specify your custom filter
