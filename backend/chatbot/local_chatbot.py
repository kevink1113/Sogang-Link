import os
import openai
from openai.types.beta.threads.runs import ToolCall, ToolCallDelta, RunStep
from typing_extensions import override
from openai import AssistantEventHandler
import time
import json

from secret import get_secret

client = openai.OpenAI(api_key=get_secret())
#######################################################################################
thread_id = ""


# 글자 로딩되는대로 한글자씩 출력해주는건데, post방식으로 어떻게 전달할지 몰라서 일단 보류해놈
class EventHandler(AssistantEventHandler):
    def __init__(self, thread_id, assistant_id):
        super().__init__()
        self.output = None
        self.tool_id = None
        self.thread_id = thread_id
        self.assistant_id = assistant_id
        self.run_id = None
        self.run_step = None
        self.function_name = ""
        self.arguments = ""

    @override
    def on_text_created(self, text) -> None:
        print(f"\n서강gpt > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call: ToolCall):
        self.tool_id = tool_call.id
        if tool_call.type == "function":
            self.function_name = tool_call.function.name

        print(f"\nassistant > {tool_call.type}\n", flush=True)

        run = client.beta.threads.runs.retrieve(
            thread_id=self.thread_id,
            run_id=self.run_id)

        while run.status in ["queued", "in_progress"]:
            run = client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=self.run_id)

    @override
    def on_tool_call_done(self, tool_call: ToolCall):
        run = client.beta.threads.runs.retrieve(
            thread_id=self.thread_id,
            run_id=self.run_id)

        if run.status == "requires_action":
            if self.function_name == "tell_secret":
                self.output = tell_secret(self.arguments)

                with client.beta.threads.runs.submit_tool_outputs_stream(
                        thread_id=self.thread_id,
                        run_id=self.run_id,
                        tool_outputs=[{
                            "tool_call_id": self.tool_id,
                            "output": self.output
                        }],
                        event_handler=EventHandler(self.thread_id, self.assistant_id)
                ) as stream:
                    stream.until_done()
            else:
                print("그런 함수는 없습니다.")
                return

    @override
    def on_tool_call_delta(self, delta: ToolCallDelta, snapshot: ToolCall):
        if delta.type == "function":
            self.arguments += delta.function.arguments

    @override
    def on_run_step_created(self, run_step: RunStep):
        self.run_id = run_step.run_id


def tell_secret(input):
    secret = "할리스 아메리카노 벤티 사이즈는" + input + "원이다"
    return json.dumps({
        "secret": secret
    })


def qstream(assistant_id, user, thread_id, question):
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=question
    )

    with client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant_id,
            event_handler=EventHandler(thread_id=thread_id, assistant_id=assistant_id)
    ) as stream:
        stream.until_done()


if __name__ == "__main__":
    while True:
        assistant_id = "asst_DkPMBJ4uoJaI7o2KPGiRqn0k"
        thread_id = client.beta.threads.create().id
        qstream(assistant_id, "", thread_id, input())
