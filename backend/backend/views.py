from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
from drf_yasg import openapi
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .crawl_saint import get_saint_cookies
from .auth_backend import PasswordlessAuthBackend
from django.contrib.auth import login as auth_login

# from backend.chatbot import chatbot_function_call
# from chatbot import chatbot_function_call
from chatbot.chatbot import chatbot_function_call


from drf_yasg.utils import swagger_auto_schema
import openai
from openai import AssistantEventHandler

from chatbot.chatbot import chatbot_query
from chatbot.chatbot import chatbot_query_stream
from chatbot.secret import get_secret
from chatbot.api import *

from django.http import StreamingHttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
import json

class LoginView(APIView):
    """
    post:
    사용자 로그인(회원가입)을 위한 엔드포인트

    username과 password를 JSON 형태로 전달받아 인증을 수행
    인증에 성공하면, 사용자 토큰을 반환

    요청 예시:
    {
        "username": "2019xxxx",
        "password": "password123"
    }

    응답 예시:
    {
        "token": "1234567890abcdef"
    }
    """

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='학번'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='비밀번호')
        }
        # response 정의

    ))
    # @swagger_auto_schema(operation_description="POST 요청을 위한 엔드포인트입니다.")
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        # print(username, password)
        cookies = get_saint_cookies(username, password)
        if cookies is None:
            return Response({'error': 'Invalid Credentials or Saint Cookies not retrieved'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = PasswordlessAuthBackend().authenticate(username=username, cookies=cookies)
        if user is None:
            return Response({'error': 'Authentication Failed'}, status=status.HTTP_404_NOT_FOUND)

        auth_login(request, user, backend='backend.auth_backend.PasswordlessAuthBackend')  # Django login

        # 토큰이 이미 존재하면 가져오고, 그렇지 않으면 생성합니다.
        token, created = Token.objects.get_or_create(user=user)
        print("Token: ", token.key, "Created: ", created)
        # 'created' 변수는 토큰이 새로 생성되었는지 여부를 나타냅니다.
        # 여기서 추가적인 로직을 구현할 수 있습니다 (예: 로그 생성).

        print(user.username, user.name, user.state, user.year, user.semester, user.major, user.advisor, user.nickname)

        return Response({'token': token.key,  # 토큰
                         'username': user.username,  # 학번
                         'name': user.name,  # 이름
                         'state': user.state,  # 0: 재학, 1: 휴학, 2: 졸업
                         'year': user.year,  # 학년
                         'semester': user.semester,  # 학기
                         'major': user.major,  # 전공
                         'advisor': user.advisor,  # 지도교수
                         'nickname': user.nickname,  # 닉네임
                         },
                        status=status.HTTP_200_OK)


def my_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cookies = get_saint_cookies(username, password)
        if cookies is None:
            return render(request, 'login.html')
        user = PasswordlessAuthBackend().authenticate(username=username, cookies=cookies)
        # login 함수 호출
        auth_login(request, user)
        return redirect('/')
    else:
        # GET 요청 처리
        pass
    return render(request, 'login.html')


def offline(request):
    return render(request, 'offline.html')


class ChatView(APIView):
    """
    post:
    챗봇 구현 예시
    요청 예시:
    {
        "question": "아메리카노와 에스프레소의 차이에 대해 알려줘"
    }
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'question': openapi.Schema(type=openapi.TYPE_STRING, description='질문')
        }
        # response 정의
    ))
    # @swagger_auto_schema(operation_description="POST 요청을 위한 엔드포인트입니다.")
    def post(self, request, *args, **kwargs):
        user = request.user

        print(user)
        print("Question: ", request.data.get('question'))

        question = request.data.get('question')
        assistant_id = "asst_fSEoeHlDpbVT7NA4chr18jLM"
        #assist 나중에 숨기거나 해야하나 안숨겨도 별 문제는 없긴함
        # thread_id = "thread_QkJXOaYm6rzUUcsF1xhZh9DU"
        thread_id = user.thread

        # ========== 그냥 한번에 버전, stream 버전 ==========

        messages = chatbot_query(assistant_id, user, thread_id, question) # TODO: chatbot_query_stream으로 변경
        # messages = chatbot_query_stream(assistant_id, user, thread_id, question)
        # chatbot_query_setrem은 message 반환 안해서 변경함
        chatbot_query_stream(assistant_id, user, thread_id, question)
        # ===================== 디버깅용 출력 =====================
        total_message = "대화:\n"
        for i, message in enumerate(reversed(messages.data), start=1):
            total_message += "서강gpt>" if message.role == "assistant" else "당신>"
            for content in message.content:
                total_message += content.text.value + "\n"
        print("total message: ", total_message)
        # ===================== 디버깅용 출력 =====================

        recent_question = messages.data[1].content[0].text.value
        recent_answer = messages.data[0].content[0].text.value

        print(recent_question)
        print(recent_answer)
        return Response({'answer': recent_answer},
                        status=status.HTTP_200_OK)
        


class StreamView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        assistant_id = "asst_fSEoeHlDpbVT7NA4chr18jLM"
        thread_id = user.thread  # Ensure user has a 'thread' attribute or handle accordingly
        question = request.data.get('question', '')

        # Setup OpenAI client
        client = openai.OpenAI(api_key=get_secret())

        # Create a message in the thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=question
        )

        def event_stream():
            # Stream the thread's run
            with client.beta.threads.runs.stream(thread_id=thread_id, assistant_id=assistant_id) as stream:
                for event in stream:
                    # Handle different types of events
                    if hasattr(event, 'status'):
                        if event.status == "completed":
                            break
                        elif event.status == "requires_action":
                            # Handle action required status
                            chatbot_function_call(event, assistant_id, user, thread_id)
                    # Send back text updates
                    if hasattr(event, 'content') and 'text' in event.content:
                        text = event.content['text']
                        yield f"data: {json.dumps({'text': text})}\n\n"

        # Set headers to notify the client that this is an event-stream.
        return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
