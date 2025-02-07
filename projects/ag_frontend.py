"""
### 需求分析
- 提供给 ag.py 调用的两个 POST 接口，一个用于更新 问，一个用于更新 答

"""

import io
import pprint
import tracemalloc
from typing import Optional
from uuid import uuid4

from loguru import logger
from nicegui import ui, app
from nicegui.element import Element
from fastapi import Request
from pydantic import BaseModel

tracemalloc.start()

log_output = io.StringIO()
logger.remove()
logger.add(log_output, format="{message}")

OPENAI_API_KEY = "!!not-set"


def push_log(log, message: str):
    logger.info(message)
    log.push(log_output.getvalue())
    log_output.close()


# @ui.page('/')
def main():
    client_id = str(uuid4())
    print(f"{client_id}: OPENAI_API_KEY: {OPENAI_API_KEY}")

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

    class RefreshAnswerRequest(BaseModel):
        question: str
        content: str

    @app.post("/api/refresh_answer2")
    def refresh_answer(request: Request, data: RefreshAnswerRequest):
        print("enter refresh_answer")

        # nonlocal response_message2, spinner2
        #
        # print(f"response_message2: {response_message2}")
        # response_message2.clear()
        # with response_message2:
        #     ui.markdown(data.content)
        # ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        # print(f"spinner2: {spinner2}")
        # message_container.remove(spinner2)

        with message_container:
            ui.chat_message(text=data.question, name='You', sent=True)
            response_message = ui.chat_message(name='Bot', sent=False)
            spinner = ui.spinner(type='dots')

        response_message.clear()
        with response_message:
            ui.markdown(data.content)
            ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        message_container.remove(spinner)

    class RefreshQuestionAnswerRequest(BaseModel):
        question: str
        answer: str

    @app.post("/api/refresh_question_answer")
    async def refresh_question_answer(request: Request, data: RefreshQuestionAnswerRequest):
        print("enter refresh_question_answer", flush=True)

        with message_container:
            ui.chat_message(text=data.question, name='You', sent=True)
            response_message = ui.chat_message(name='Bot', sent=False)
            spinner = ui.spinner(type='dots')

        response_message.clear()
        with response_message:
            ui.markdown(data.content)
            await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        message_container.remove(spinner)

        print(1111111111111111111111111111111)

    async def send() -> None:
        question = text.value
        text.value = ''

        with message_container:
            ui.chat_message(text=question, name='You', sent=True)
            response_message = ui.chat_message(name='Bot', sent=False)
            spinner = ui.spinner(type='dots')

        try:
            response = ''
            async for chunk in llm.astream(question, config={'callbacks': [NiceGuiLogElementCallbackHandler(log)]}):
                response += chunk.content
                response_message.clear()
                with response_message:
                    ui.html(response)
                await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
            message_container.remove(spinner)
        except Exception as e:
            push_log(log, f"{e}")
            raise e

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
            text = ui.input(placeholder=placeholder).props('rounded outlined input-class=mx-3') \
                .classes('w-full self-center').on('keydown.enter', lambda: ...)  # send
        ui.markdown('simple chat app built with [NiceGUI](https://nicegui.io)') \
            .classes('text-xs self-end mr-8 m-[-1em] text-primary')

    print(pprint.pformat([e.path for e in app.routes]))
    # await ui.context.client.connected()
    ui.notify("client connected")

main()
ui.run(title='Chat with GPT-3 (example)', host="localhost", port=9000, reload=False, show=False)
