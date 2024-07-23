from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from .models import Notice
from .serializers import NoticeSerializer

from .fcm import send_topic_notification

class NoticeViewSet(APIView):
    # permission_classes = [IsAuthenticated]  # Apply any permissions you deem necessary

    @swagger_auto_schema(operation_description="Get a list of all notices or filter them by 'board'")
    def get(self, request):
        board = request.query_params.get('board')
        if board:
            notices = Notice.objects.filter(board=board).order_by("-date")
        else:
            notices = Notice.objects.all()
        
        serializer = NoticeSerializer(notices, many=True)
        return Response(serializer.data)

    # @swagger_auto_schema(operation_description="Create a new notice")
    # def post(self, request):
    #     serializer = NoticeSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=201)
    #     return Response(serializer.errors, status=400)


def notify_topic(request):
    # 예제 토픽, 실제로는 요청 데이터나 기타 로직에 따라 토픽을 설정해야 함
    topic = 'general_notifications'
    title = '공지사항'
    body = '새로운 공지사항이 있습니다.'
    
    # 추가 데이터 (선택 사항)
    data = {
        'key1': 'value1',
        'key2': 'value2',
    }
    print("notify_topic")
    send_topic_notification(topic, title, body, data)
    return JsonResponse({'status': 'success'})