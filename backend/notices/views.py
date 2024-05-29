from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notice
from .serializers import NoticeSerializer

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
