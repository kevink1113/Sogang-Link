import os
import openai
from openai.types.beta.threads.runs import ToolCall, RunStep
from typing_extensions import override
from openai import AssistantEventHandler
import time
import json

from chatbot.secret import get_secret
from chatbot.api import *

client = openai.OpenAI(api_key=get_secret())
#######################################################################################

'''
#글자 로딩되는대로 한글자씩 출력해주는건데, post방식으로 어떻게 전달할지 몰라서 일단 보류해놈
class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\n서강gpt > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)


def query_stream(assistant_id, user, thread_id, question):
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=question
    )
    with client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant_id,
            event_handler=EventHandler(),
    ) as stream:
        stream.until_done()
'''


'''
외부 api 목록
def get_user_info(username):
    return User.objects.get(username=username)

def get_course_info():
    return Course.objects.all()

def get_takes_info():
    return Takes.objects.all()
'''


def chatbot_function_call(runs, assistant_id, user, thread_id):
    tools = runs.required_action.submit_tool_outputs.tool_calls
    tool_outputs = []
    for tool in tools:
        tool_id = tool.id

        action = tool.function.name
        data = ""
        if action == "get_user_info":
            data = get_user_info(user.username)
        elif action == "get_course_info":
            data = get_course_info()
        elif action == "get_takes_info":
            data = get_takes_info(user.username)
        elif action == "get_current_info":
            data = get_current_info(user.username)
        tool_outputs.append({
                "tool_call_id": tool_id,
                "output": json.dumps(data)
            })

    runs = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=runs.id,
        tool_outputs=tool_outputs
    )


def cancel_active_runs(client, thread_id):
    """
    명시된 thread에서 실행중인 모든 run을 취소하는 함수

    :param client: 사용할 OpenAI client
    :param thread_id: 실행중인 active run(들)이 있는 thread ID
    """

    active_runs = client.beta.threads.runs.list(thread_id=thread_id).data
    for run in active_runs:
        if run.status not in ["completed", "failed", "cancelled", "expired"]: # 취소된 run은 다시 취소하지 않음
            client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run.id)
            print(f"Cancelled run {run.id}")


def chatbot_query(assistant_id, user, thread_id, question):
    # 만약 이전에 진행중인 run이 있다면 취소
    # 이거 오류 나서 지움. 쿼리 실행에 필요한 함수는 아니니까 일단 지웠고, 나중에 내가 고칠테니까 신경안써도 ㄱㅊ
    # cancel_active_runs(client, thread_id)

    # 클리어 한 다음 새로운 질문을 추가
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=question
    )

    # 새로운 run 생성
    runs = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    # run이 완료되거나 실패할 때까지 기다림
    while runs.status not in ["completed", "failed"]:
        if runs.status == "requires_action": # 만약 function call이 필요하다면
            chatbot_function_call(runs, assistant_id, user, thread_id)
        runs = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=runs.id)

    # run이 완료되면 메시지 반환
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    return messages



class EventHandler(AssistantEventHandler):
    def __init__(self, thread_id, assistant_id, user):
        super().__init__()
        self.thread_id = thread_id
        self.assistant_id = assistant_id
        self.run_id = None
        self.user = user
        self.tool_outputs = []

    @override
    def on_text_created(self, text) -> None:
        print(f"\n서강gpt > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    @override
    def on_tool_call_done(self, tool_call: ToolCall):
        # run 참조
        run = client.beta.threads.runs.retrieve(
            thread_id=self.thread_id,
            run_id=self.run_id)
        # 처음 tool_call에서 모든 tool_call을 처리
        if run.status == "requires_action":
            tools = run.required_action.submit_tool_outputs.tool_calls
            for tool in tools:
                tool_id = tool.id
                function_args = tool.function.arguments
                function_name = tool.function.name
                data = ""

                #함수 하드 코딩 안 하는 방법이 있긴 한데, 좀 가독성이 구려서 그냥 하드코딩 합시다.
                if function_name == "get_user_info":
                    data = get_user_info(self.user.username)
                elif function_name == "get_course_info":
                    data = get_course_info()
                elif function_name == "get_takes_info":
                    data = get_takes_info(self.user.username)
                self.tool_outputs.append({
                    "tool_call_id": tool_id,
                    "output": json.dumps(data)
                })
            #스트림으로 보내기
            with client.beta.threads.runs.submit_tool_outputs_stream(
                    thread_id=self.thread_id,
                    run_id=self.run_id,
                    tool_outputs=self.tool_outputs,
                    event_handler=EventHandler(self.thread_id, self.assistant_id, self.user)
            ) as stream:
                stream.until_done()

    @override
    def on_run_step_created(self, run_step: RunStep):
        # run_id 저장
        self.run_id = run_step.run_id

def chatbot_query_stream(assistant_id, user, thread_id, question):
    # 질문 보내기
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=question
    )
    # 스트림으로 받기
    with client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant_id,
            event_handler=EventHandler(thread_id=thread_id, assistant_id=assistant_id, user=user),
    ) as stream:
        stream.until_done()
    