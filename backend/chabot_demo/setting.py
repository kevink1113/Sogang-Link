import os
import openai

os.environ["OPENAI_API_KEY"] = "채웡"
client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
#######################################################################################


def create_assistant(files):
    # 업로드 할 파일들 모으기
    file = []
    for f in files:
        with open(f, "rb") as file_data:
            file_response = client.files.create(file=file_data, purpose="assistants")
            file += [file_response.id]

    # 어시스턴트 생성
    assistant = client.beta.assistants.create(
        name="Sogang Gpt",
        instructions="스마트한 학교 생활 도우미. 서강대학교의 다양한 학교 정보를 알려준다. 이름은 Sogang gpt.",
        model="gpt-4-1106-preview",
        tools=[{"type": "retrieval"}],
        file_ids=file,
    )

    return assistant


def create_thread():
    thread = client.beta.threads.create()
    return thread
