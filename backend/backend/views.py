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

import openai
from chatbot.secret import get_secret
from chatbot.api import *

from django.contrib.auth import login as auth_login
from typing_extensions import override
from openai.types.beta.threads.runs import ToolCall, RunStep

from openai.types.beta.assistant_stream_event import (
    ThreadRunRequiresAction, ThreadMessageDelta, ThreadRunCompleted,ThreadMessageCompleted,
    ThreadRunFailed, ThreadRunCancelling, ThreadRunCancelled, ThreadRunExpired, ThreadRunStepFailed,
    ThreadRunStepCancelled)
# from backend.chatbot import chatbot_function_call
# from chatbot import chatbot_function_call
from chatbot.chatbot import chatbot_function_call

client = openai.OpenAI(api_key=get_secret())

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

def cancel_active_runs(client, thread_id):
    """
    명시된 thread에서 실행중인 모든 run을 취소하는 함수

    :param client: 사용할 OpenAI client
    :param thread_id: 실행중인 active run(들)이 있는 thread ID
    """

    active_runs = client.beta.threads.runs.list(thread_id=thread_id).data
    for run in active_runs:
        if run.status not in ["completed", "failed", "cancelled", "expired", "incomplete"]: # 취소된 run은 다시 취소하지 않음
            client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run.id)
            print(f"Cancelled run {run.id}")


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

    def post(self, request, *args, **kwargs):
        user = request.user
        question = request.data.get('question')
        print("Question recieved: ", question)
        assistant_id = "asst_fSEoeHlDpbVT7NA4chr18jLM"

        # thread_id = client.beta.threads.create().id#user.thread
        thread_id = user.thread
        # Initialize the streaming process
        # 질문 보내기

        # cancel_active_runs(client, thread_id)
        # print("Active runs cancelled")


        cancel_active_runs(client, thread_id)
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=question
        )
        def event_stream():

            # 스트림으로 받기

            with client.beta.threads.runs.stream(
                    thread_id=thread_id,
                    assistant_id=assistant_id
            ) as stream:
                print("Stream started")
                try:
                    for event in stream:
                        # print(event, end="\n\n")
                        if isinstance(event, ThreadMessageDelta):   # 메시지 델타 이벤트 처리
                            data = event.data.delta.content
                            for text in data:
                                print(text.text.value, end='', flush=True)
                                yield f"data: {json.dumps({'text': text.text.value})}\n\n"

                        elif isinstance(event, ThreadRunRequiresAction):
                            run = event.data
                            tools = run.required_action.submit_tool_outputs.tool_calls
                            tool_outputs = []
                            for tool in tools:
                                tool_id = tool.id
                                function_args = tool.function.arguments
                                function_name = tool.function.name
                                data = ""
                                print("++++++++++ Function called: ", function_name, "++++++++++++")

                                # 함수 하드 코딩 안 하는 방법이 있긴 한데, 좀 가독성이 구려서 그냥 하드코딩 합시다.
                                function_args = json.loads(function_args)

                                # semester = None
                                # if(function_args.get('semester') != None):
                                #     semester = function_args['semester']
                                # # Use function_args in the function call

                                if function_name == "get_user_info":
                                    data = get_user_info(user.username)
                                elif function_name == "get_course_info":
                                    data = get_course_info(
                                        semester=function_args.get('semester', ""),
                                        name=function_args.get('name', ""),
                                        credit=function_args.get('credit', ""),
                                        day=function_args.get('day', ""),
                                        classroom=function_args.get('classroom', ""),
                                        advisor=function_args.get('advisor', ""),
                                        major=function_args.get('major', "")
                                    )
                                elif function_name == "get_takes_info":
                                    data = get_takes_info(
                                        username=user.username, 
                                        semester=function_args.get('semester', ""),
                                        final_grade=function_args.get('final_grade', "")
                                    )
                                elif function_name == "get_empty_classrooms":
                                    data = get_empty_classrooms(function_args['building'])
                                elif function_name == "get_current_info":
                                    data = get_current_info(user.username)
                                elif function_name == "get_building_info":
                                    building_name = function_args.get('building_name', "")
                                    data = get_building_info(building_name)
                                elif function_name == "get_facility_info":
                                    facility_name = function_args.get('facility_name', "")
                                    data = get_facility_info(facility_name)
                                elif function_name == "get_menu_info":
                                    facility_name = function_args.get('facility_name', "")
                                    date = function_args.get('date', "")
                                    data = get_menu_info(facility_name, date)
                                elif function_name == "get_filtered_restaurants":
                                    name = function_args.get('name', "")
                                    category = function_args.get('category', "")
                                    place = function_args.get('place', "")
                                    min_price = function_args.get('min_price', None)
                                    max_price = function_args.get('max_price', None)
                                    tag = function_args.get('tag', "")
                                    data = get_filtered_restaurants(name, category, place, min_price, max_price, tag)


                                tool_outputs.append({
                                    "tool_call_id": tool_id,
                                    "output": json.dumps(data)
                                })
                            # 스트림으로 보내기
                            with client.beta.threads.runs.submit_tool_outputs_stream(
                                    thread_id=run.thread_id,
                                    run_id=run.id,
                                    tool_outputs=tool_outputs
                            ) as stream2:
                                for event2 in stream2:
                                    if isinstance(event2, ThreadMessageDelta):
                                        # 메시지 델타 이벤트 처리
                                        data = event2.data.delta.content
                                        for text in data:
                                            print(text.text.value, end='', flush=True)
                                            yield f"data: {json.dumps({'text': text.text.value})}\n\n"

                        elif isinstance(event, ThreadRunCompleted):
                            # 실행 완료 이벤트 처리
                            yield "data: run_completed\n\n"
                except GeneratorExit:
                    # Handle the case when the client disconnects
                    stream.close()


        # Return a StreamingHttpResponse that keeps the connection open
        response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        return response


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
