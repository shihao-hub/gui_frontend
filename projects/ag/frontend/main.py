"""
### 需求分析
- 提供给 main.py 调用的两个 POST 接口，一个用于更新 问，一个用于更新 答

"""
from aiohttp import ClientResponse


def bat_setup():
    import sys
    from pathlib import Path

    # 获取当前文件的绝对路径，然后定位到 gui_frontend 目录
    current_dir = Path(__file__).resolve().parent
    frontend_dir = current_dir.parent.parent.parent  # 根据层级调整
    sys.path.append(str(frontend_dir))


bat_setup()

import functools
import io
import pprint
import re
import tracemalloc
from types import SimpleNamespace
from typing import Optional, TypedDict, Dict
from uuid import uuid4

import aiohttp
from loguru import logger

from nicegui import ui, app
from nicegui.element import Element
from nicegui.events import GenericEventArguments
from fastapi import Request
from pydantic import BaseModel

# todo: projects 找不到
# todo: python + docker
from projects.ag import configs

tracemalloc.start()

log_output = io.StringIO()
logger.remove()
logger.add(log_output, format="{message}")

OPENAI_API_KEY = "!!not-set"


def push_log(log, message: str):
    logger.info(message)
    log.push(log_output.getvalue())
    log_output.close()


def catch_unexpected_exception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return 500, {"message": f"Error: {e}"}

    return wrapper


# @ui.page('/')
def main():
    client_id = str(uuid4())

    # print(f"{client_id}: OPENAI_API_KEY: {OPENAI_API_KEY}")

    class RefreshQuestionRequest(BaseModel):
        question: str

    response_message2: Optional[Element] = None
    spinner2: Optional[Element] = None

    @app.post("/api/refresh_question2")
    async def refresh_question(request: Request, data: RefreshQuestionRequest):
        print("enter refresh_question")
        nonlocal response_message2, spinner2

        print(f"response_message: {response_message2}")
        with message_container:
            ui.chat_message(text=data.question, name='You', sent=True)
            response_message = ui.chat_message(name='Bot', sent=False)
            spinner = ui.spinner(type='dots')
            response_message2 = response_message
            spinner2 = spinner
        print(f"response_message: {response_message2}")

    class RefreshQuestionAnswerRequest(BaseModel):
        question: Optional[str] = ""
        content: Optional[str] = ""
        stream: bool = False

    class RefreshQuestionAnswerRefType(TypedDict):
        response_message: Optional[Element]
        spinner: Optional[Element]
        markdown: Optional[Element]

    refresh_question_answer_ref: RefreshQuestionAnswerRefType = {
        "response_message": None,
        "spinner": None,
        "markdown": None,
    }

    @app.post("/api/refresh_question_answer")
    @catch_unexpected_exception
    def refresh_question_answer(request: Request, data: RefreshQuestionAnswerRequest):
        ref = refresh_question_answer_ref

        print(f"question: {bool(data.question)}, "
              f"content: {bool(data.content)}, "
              f"stream: {bool(data.stream)}")

        if data.question:
            with message_container:
                ui.chat_message(text=data.question.strip(), name='You', sent=True)
                response_message = ui.chat_message(name='Bot', sent=False)
                spinner = ui.spinner(type='dots')
                ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
                ref["response_message"] = response_message
                ref["spinner"] = spinner
        elif data.content:
            try:
                response_message = ref["response_message"]
                spinner = ref["spinner"]

                response_message.clear()
                with response_message:
                    content = data.content
                    pattern = re.compile(r"<think>.*</think>", re.S)
                    match = pattern.match(content)
                    if match:
                        end = match.span()[1]
                        content = content[:end] + "\n\n---\n\n" + content[end:]
                    markdown = ui.markdown(content)
                    ref["markdown"] = markdown
                    ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
                message_container.remove(spinner)
            finally:
                ref["response_message"] = None
                ref["spinner"] = None
        elif data.stream:
            try:
                markdown = ref["markdown"]

                markdown.content = markdown.content + "\n" + data.content
                markdown.update()
            finally:
                ref["markdown"] = None
        return 200

    async def invoke_ai_api(question: str) -> ClientResponse:
        url = configs.SERVER_BASE_URL + "/api/invoke_ai_api"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"question": question}) as response:
                # todo: 超时怎么办
                return response

    async def send(event: GenericEventArguments) -> None:
        key_event: Dict = event.args
        # print(type(key_event))
        # print(key_event)

        if key_event.get("key") != "Enter":
            return

        # enter 发送，ctrl + enter 换行
        if not key_event.get("ctrlKey"):
            text.value += "\n"
            text.update()
            return

        question = text.value

        text.value = ""

        # with message_container:
        #     ui.chat_message(text=question, name='You', sent=True)
        #     response_message = ui.chat_message(name='Bot', sent=False)
        #     spinner = ui.spinner(type='dots')

        # 调用 问答 接口
        response = await invoke_ai_api(question)
        print(response)
        # response_message.clear()
        # with response_message:
        #     content = await response.content.read()
        #     ui.markdown(content.decode("utf-8"))
        #     await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        # message_container.remove(spinner)

    ui.add_css(r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}')

    # the queries below are used to expand the contend down to the footer (content can then use flex-grow to expand)
    ui.query('.q-page').classes('flex')
    ui.query('.nicegui-content').classes('w-full')

    with ui.tabs().classes('w-full') as tabs:
        chat_tab = ui.tab('Chat')
        logs_tab = ui.tab('Logs')
    with ui.tab_panels(tabs, value=chat_tab).classes('w-full max-w-2xl mx-auto flex-grow items-stretch'):
        message_container = ui.tab_panel(chat_tab).classes('items-stretch')
        with ui.tab_panel(logs_tab):
            log = ui.log().classes('w-full h-full')

    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            placeholder = 'message' if OPENAI_API_KEY != 'not-set' else \
                'Please provide your OPENAI key in the Python script first!'
            text = ui.textarea(placeholder=placeholder).props('rounded outlined input-class=mx-3') \
                .classes('w-full self-center').on('keydown', send)  # send | lambda: ...
        ui.markdown('simple chat app built with [NiceGUI](https://nicegui.io)') \
            .classes('text-xs self-end mr-8 m-[-1em] text-primary')

    # print(pprint.pformat([e.path for e in app.routes]))
    # await ui.context.client.connected()
    # ui.notify("client connected")


main()

ui.run(title="Chat with DeepSeek-R1",
       host=configs.CLIENT_HOST,
       port=configs.CLIENT_PORT,
       reload=False,
       show=False)
