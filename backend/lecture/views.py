from drf_yasg import openapi
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Takes
from .serializers import CourseSerializer, TakesSerializer
from django.shortcuts import get_object_or_404

from drf_yasg.utils import swagger_auto_schema


# This code uses the `csv` module to read the data from the `classrooms.csv` file. 
# It then iterates over each row of the CSV file and processes the data to import the classrooms into the system. 
# You will need to replace the comments with the actual code to perform the necessary operations 
# for importing the classrooms.

classrooms = ["[AS109]","[AS111]","[AS301]","[AS303]","[AS305]","[AS311]","[AS412]","[AS414]","[AS510]","[AS611]","[AS612]","[AS714]","[AS912]",
        "[D104B]","[D105]","[D202]","[D301]","[D302]","[D303A]","[D303B]","[D304]","[D401A]","[D402]","[D406]","[D412]","[D502]","[D503]","[D504]","[DB101]","[DB102]",
        "[F401]",
        "[GA303B]","[GA305]","[GA401]","[GA402]","[GA403]","[GA404]","[GA505]","[GA506]",
        "[GN101]","[GN102]","[GN201]","[GN202]","[GN203]","[GN301]","[GN304]","[GN311]",
        "[J102]","[J104]","[J106]","[J107]","[J108]","[J109]","[J110]","[J112]","[J114]","[J116]","[J118]","[J120]","[J128]","[J202]","[J204]","[J207]","[J209]","[J211]",
        "[J215]","[J217]","[J219]","[J302]","[J307]","[J309]","[J311]","[J313]","[J315]","[J317]","[J319]","[J321]","[J323]","[J325]","[J327]","[J602]","[J609]","[J616]",
        "[K201]","[K202]","[K203]","[K204]","[K207]","[K208]","[K212]","[K213]","[K301]","[K302]","[K303]","[K304]","[K305]","[K306]","[K307]","[K309]","[K401]","[K402]",
        "[K403]","[K404]","[K405]","[K406]","[K407]","[K501]","[K502]","[K503]","[K504]","[K506]","[K507]",
        "[MA102]","[MA104]","[MA106]","[MA201]","[MA202]","[MA203]","[MA204]","[MA206]","[MA208]","[MA308]","[MA610]",
        "[PA101]","[PA201]","[PA203]","[PA405]",
        "[R103]","[R107]","[R108]","[R110]","[R112]","[R113]","[R114]","[R115]","[R117]","[R119]","[R1418]","[R204]","[R210]","[R404]","[R405]","[R708]","[R712]","[R714]","[R903]","[R914]",
        "[RA110A]","[RA204]","[RA205]","[RA308]","[RA310]","[RA406A]","[RA406B]","[RA408]","[RA410]",
        "[X229]","[X238]","[X349]","[X353]","[X423]","[X426]","[X427]","[X428]","[X429]","[X430]","[X513]","[X514]"]

# Create your views here.
from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer
import datetime
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    # @swagger_auto_schema(operation_description="courses(개설교과목) GET 요청을 위한 엔드포인트")
    def get_queryset(self):
        queryset = Course.objects.all()
    
        semester = self.request.query_params.get('semester')
        name = self.request.query_params.get('name')
        credit= self.request.query_params.get('credit')
        day = self.request.query_params.get('day')
        classroom = self.request.query_params.get('classroom')
        advisor = self.request.query_params.get('advisor')
        major = self.request.query_params.get('major')

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

        return queryset


class StudentTakesListView(APIView):
    
    """
    get:
    현재 로그인한 학생이 수강한 과목 목록을 조회합니다.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="takes(수강목록) GET 요청을 위한 엔드포인트")
    def get(self, request):
        takes = Takes.objects.filter(student=request.user)
        
        semester = request.query_params.get('semester')
        day = request.query_params.get('day')
        credit = request.query_params.get('credit')
        name = request.query_params.get('name')
        major = request.query_params.get('major')
        real = request.query_params.get('real')
        
        if semester:
            takes = takes.filter(student=request.user, course__semester=semester)
        if day:
            takes = takes.filter(student=request.user, course__day__icontains=day)
        if credit:
            takes = takes.filter(student=request.user, course__credit=credit)
        if name:
            takes = takes.filter(student=request.user, course__name__icontains=name)
        if major:
            takes = takes.filter(student=request.user, course__major__icontains=major)
        if real:
            takes = takes.filter(student=request.user, real=real)
        # student = request.user
        # takes = Takes.objects.filter(student=student)
        serializer = TakesSerializer(takes, many=True)
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        course_serializer = CourseSerializer(data=request.data)
        if course_serializer.is_valid():
            if self.has_time_conflicts(course_serializer.validated_data, request.user):
                return Response({'error': 'Time conflict with another course.'}, status=status.HTTP_400_BAD_REQUEST)
            
            course = course_serializer.save()
            new_take = Takes()
            new_take.course = course
            new_take.student = request.user
            new_take.day = request.data.get('day', '')
            new_take.classroom = request.data.get('classroom', '')
            new_take.start_time = request.data.get('start_time', datetime.time(0, 0))
            new_take.end_time = request.data.get('end_time', datetime.time(0, 0))
            new_take.real = request.data.get('real', False)
            new_take.middle_grade = request.data.get('middle_grade', '')
            new_take.final_grade = request.data.get('final_grade', '')
            new_take.save()

            print("Added new take: ", new_take.course)
            return Response(TakesSerializer(new_take).data, status=status.HTTP_201_CREATED)

    def put(self, request, pk, *args, **kwargs):
        take = get_object_or_404(Takes, pk=pk, student=request.user)
        course_serializer = CourseSerializer(take.course, data=request.data, partial=True)

        if course_serializer.is_valid():
            if self.has_time_conflicts(course_serializer.validated_data, request.user, excluding_take_id=take.id):
                return Response({'error': 'Time conflict with another course.'}, status=status.HTTP_400_BAD_REQUEST)

            course_serializer.save()
            take_serializer = TakesSerializer(take, data=request.data, partial=True)
            if take_serializer.is_valid():
                take_serializer.save()
                return Response(take_serializer.data)
            else:
                return Response(take_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(course_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            take = get_object_or_404(Takes, pk=pk, student=request.user)
            take.delete()
            return Response({'Take deleted'})
        except:
            return Response({'error': 'Take not found.'}, status=status.HTTP_404_NOT_FOUND)


    def has_time_conflicts(self, validated_data, user, excluding_take_id=None):
        # Extract course schedule data
        day = validated_data.get('day')
        start_time = validated_data.get('start_time')
        end_time = validated_data.get('end_time')

        # Query to check for overlaps
        query = Takes.objects.filter(
            student=user,
            course__day=day,
            course__start_time__lt=end_time,
            course__end_time__gt=start_time
        )

        if excluding_take_id:
            query = query.exclude(id=excluding_take_id)

        return query.exists()

class SemesterTakesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, semester, format=None):
        takes = Takes.objects.filter(course__semester=semester)
        serializer = TakesSerializer(takes, many=True)
        return Response(serializer.data)

