"""
### 总结
1. 本页面是个简单的 ai 聊天应用。在实现的过程中发现，css 很重要，页面不好看是不行的。

   其次是关于优化，nicegui 优化起来不够灵活，真要做出不只是玩具的 web 应用，还得是 js css html！
2.

"""

import asyncio
import os
import traceback
from typing import Dict, Any, Optional, List, AsyncGenerator

import httpx
from openai import AsyncOpenAI
from loguru import logger
from dotenv import load_dotenv

from nicegui import ui
from nicegui.events import GenericEventArguments

from . import configs

load_dotenv()  # 加载 .env 文件

DEEP_SEEK_API_KEY = os.getenv("DEEP_SEEK_API_KEY", default="not-set")


# 全局上下文存储
class ConversationManager:
    DEFAULT_MAX_HISTORY = 6  # 保留最近6组对话

    def __init__(self, max_history=None):
        self.history: List[Dict] = []
        self.max_history = max_history if max_history else ConversationManager.DEFAULT_MAX_HISTORY

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        # 保持历史记录长度
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-self.max_history * 2:]
            logger.info(f"保持历史记录长度，删除旧的对话")


class ChatDeepSeekAI:
    def __init__(self,
                 deepseek_api_key: str,
                 *,
                 model_name: str = configs.DEEP_SEEK_MODEL_NAME,
                 streaming: bool = True):
        self.base_url = configs.DEEP_SEEK_BASE_URL

        self.deepseek_api_key = deepseek_api_key
        self.model_name = model_name
        self.streaming = streaming

        # self.client = AsyncOpenAI(api_key=self.deepseek_api_key, base_url=self.base_url)
        self.client = AsyncOpenAI(api_key=self.deepseek_api_key, base_url=self.base_url,
                                  http_client=httpx.AsyncClient(verify=False))  # verify=False 为临时改动，生产环境不允许
        self.conversation = ConversationManager()

    async def astream(self,
                      question: str,
                      config: Optional[Dict] = None) -> AsyncGenerator[str, None]:
        config = config if config else {}
        callbacks = config.get("callbacks", [])

        try:
            # 添加用户消息到上下文
            self.conversation.add_message("user", question)

            stream = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "你是有帮助的助手，用简洁的markdown回答"},
                    *self.conversation.history[-ConversationManager.DEFAULT_MAX_HISTORY:]  # 携带最近3组对话历史
                ],
                stream=True,
                temperature=1.3,  # https://api-docs.deepseek.com/zh-cn/quick_start/parameter_settings
            )

            full_response = []
            async for chunk in stream:
                content = chunk.choices[0].delta.content  # 深度思考的思考过程这里没有获取，这对于用户来说响应时间太长了！
                if content:
                    full_response.append(content)
                    yield content
            # 添加助手回复到上下文:假如执行完此处出错会发生什么？
            if full_response:
                self.conversation.add_message("assistant", "".join(full_response))
        except Exception as e:
            logger.error(f"{e}\n{traceback.format_exc()}")
            error_msg = f"❌ 请求失败: {str(e)}"
            yield error_msg
            self.conversation.add_message("assistant", error_msg)


@ui.page(configs.PAGE_PATH, title=configs.PAGE_TITLE)
async def copilot():
    # todo: ui.page 会导致刷新页面就没了怎么办？

    # todo: 弄懂 ChatOpenAI 这个库的实现原理，这样调用 ai 接口就能得心应手了
    _llm: Optional[ChatDeepSeekAI] = None

    def get_llm_singleton():
        """
        懒加载，避免第一次进入页面时，加载过慢的问题。
        优化方向：页面加载完毕后主动初始化，而不是用户第一次发送的时候初始化
        """
        nonlocal _llm
        if _llm is None:
            _llm = ChatDeepSeekAI(DEEP_SEEK_API_KEY)
        return _llm

    async def send(event: GenericEventArguments) -> None:
        key_event: Dict = event.args
        if key_event.get("key") != "Enter":  # 没按 Enter 就无事发生
            return
        if not key_event.get("ctrlKey"):  # ctrl + enter 才发送
            text.value += "\n"
            text.update()
            return

        try:
            text.disable()

            question = text.value.strip()
            text.value = ''

            if not question:
                return

            with message_container:
                ui.chat_message(text=question, name='You', sent=True)
                response_message = ui.chat_message(name='Bot', sent=False)
                spinner = ui.spinner(type='dots')

            # todo: 此处每次都清空，性能似乎不行。这也导致未执行完不能复制，因此必须优化！
            response = ''
            async for chunk in get_llm_singleton().astream(question):
                response += chunk
                response_message.clear()
                with response_message:
                    ui.markdown(response).classes('text-wrap')
                # await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
                await asyncio.sleep(0.05)  # 控制更新频率
            message_container.remove(spinner)
        finally:
            text.enable()

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
            # todo: use it, loging record.
            log = ui.log().classes('w-full h-full')

    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            placeholder = '有问题，尽管问，enter 换行，ctrl + enter 发送' if DEEP_SEEK_API_KEY != 'not-set' else \
                'Please provide your DEEP_SEEK_API_KEY in the Python script first!'
            text = ui.textarea(placeholder=placeholder).props('rounded outlined rows=3 input-class=mx-3') \
                .classes('w-full self-center').on('keydown', send)
            if DEEP_SEEK_API_KEY == 'not-set':
                text.disable()
        # todo: 添加停止响应功能
        # ui.markdown('simple chat app built with [NiceGUI](https://nicegui.io)') \
        #     .classes('text-xs self-end mr-8 m-[-1em] text-primary')
