from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Takes
from .serializers import TakesSerializer

from drf_yasg.utils import swagger_auto_schema

# Create your views here.
from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer


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
        course_id = self.request.query_params.get('course_name')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset


class StudentTakesListView(APIView):
    """
    get:
    현재 로그인한 학생이 수강한 과목 목록을 조회합니다.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="takes(수강목록) GET 요청을 위한 엔드포인트")
    def get(self, request):
        student = request.user
        takes = Takes.objects.filter(student=student)
        serializer = TakesSerializer(takes, many=True)
        return Response(serializer.data)


class SemesterTakesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, semester, format=None):
        takes = Takes.objects.filter(course__semester=semester)
        serializer = TakesSerializer(takes, many=True)
        return Response(serializer.data)
