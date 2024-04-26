from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Takes
from .serializers import TakesSerializer

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

class CourseViewSet(viewsets.ModelViewSet):
    """
    TODO: 아직 전체 과목 목록 불러오기만 구현됨. 나머지 기능 구현 필요
    API endpoint that allows courses to be viewed or edited.

    list:
    모든 강의를 조회합니다.

    retrieve:
    특정 강의를 조회합니다.

    create:
    새로운 강의를 추가합니다.

    update:
    특정 강의를 수정합니다.

    delete:
    특정 강의를 삭제합니다.


    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    @swagger_auto_schema(operation_description="courses(개설교과목) GET 요청을 위한 엔드포인트")
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



    # def get(self, request):
    #     board = request.query_params.get('board')
    #     if board:
    #         notices = Notice.objects.filter(board=board)
    #     else:
    #         notices = Notice.objects.all()
        
    #     serializer = NoticeSerializer(notices, many=True)
    #     return Response(serializer.data)

class SemesterTakesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, semester, format=None):
        takes = Takes.objects.filter(course__semester=semester)
        serializer = TakesSerializer(takes, many=True)
        return Response(serializer.data)

