import os
import openai
from typing_extensions import override
from openai import AssistantEventHandler
import time

if __name__ == "__main__":
    from secret import get_secret
else:
    from chatbot.secret import get_secret

client = openai.OpenAI(api_key=get_secret())
#######################################################################################


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

def query(assistant_id, user, thread_id, question):
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
        runs = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=runs.id
        )
        time.sleep(0.3)
    messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
    return messages

def loop(a_id, t_id):
    while True:
        print("당신>", end="")
        query(a_id, 0, t_id, input())
        print("\n")


def main():
    assistant_id = "asst_fSEoeHlDpbVT7NA4chr18jLM"
    thread_id = "thread_4reMLnevRyGmeMxf7WnGfJ6W"
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    os.system("cls")
    for i, message in enumerate(reversed(messages.data), start=1):
        print("서강gpt>" if message.role == "assistant" else "당신>", end="")
        for content in message.content:
            print(content.text.value+"\n")
    loop(assistant_id, thread_id)


if __name__ == "__main__":
    #main()

    assistant_id = "asst_fSEoeHlDpbVT7NA4chr18jLM"
    thread_id = "thread_kh4a6S64esnKDfue5DqGvFGM"
    messages = query(assistant_id, 0, thread_id, "카라멜 마키야토 맛잇어?")
    for i, message in enumerate(reversed(messages.data), start=1):
        print("서강gpt>" if message.role == "assistant" else "당신>", end="")
        for content in message.content:
            print(content.text.value + "\n")

