import os
import openai
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
        tool_outputs.append({
                "tool_call_id": tool_id,
                "output": json.dumps(data)
            })

    runs = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=runs.id,
        tool_outputs=tool_outputs
    )


def chatbot_query(assistant_id, user, thread_id, question):
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=question
    )
    runs = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
    )
    while runs.status != "completed":
        if runs.status == "requires_action":
            chatbot_function_call(runs, assistant_id, user, thread_id)
        runs = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=runs.id
        )
        # time.sleep(0.5)
    messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
    return messages


class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\n서강gpt > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

def chatbot_query_stream(assistant_id, user, thread_id, question):
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
    