from typing import Dict, Any, Optional

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish
from langchain_openai import ChatOpenAI

from nicegui import ui

from . import configs

OPENAI_API_KEY = 'not-set'  # TODO: set your OpenAI API key here


class NiceGuiLogElementCallbackHandler(BaseCallbackHandler):
    """ Callback Handler that writes to a log element. """

    def __init__(self, log_element: ui.log) -> None:
        """Initialize callback handler."""
        self.log = log_element

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we are entering a chain."""
        self.log.push(f'\n\n> Entering new {serialized["id"][-1]} chain...')

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain."""
        self.log.push('\n> Finished chain.')
        self.log.push(f'\nOutputs: {outputs}')

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action."""
        self.log.push(action.log)

    def on_tool_end(self,
                    output: str,
                    observation_prefix: Optional[str] = None,
                    llm_prefix: Optional[str] = None,
                    **kwargs: Any,
                    ) -> None:
        """If not the final action, print out observation."""
        if observation_prefix is not None:
            self.log.push(f'\n{observation_prefix}')
        self.log.push(output)
        if llm_prefix is not None:
            self.log.push(f'\n{llm_prefix}')

    def on_text(self, text: str, **kwargs: Any) -> None:
        """Run when agent ends."""
        self.log.push(text)

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Run on agent end."""
        self.log.push(finish.log)


@ui.page(configs.PAGE_PATH, title=configs.PAGE_TITLE)
async def copilot():
    # todo: 弄懂 ChatOpenAI 这个库的实现原理，这样调用 ai 接口就能得心应手了
    _llm: Optional[ChatOpenAI] = None

    def get_llm_singleton():
        """
        懒加载，避免第一次进入页面时，加载过慢的问题。
        优化方向：页面加载完毕后主动初始化，而不是用户第一次发送的时候初始化
        """
        nonlocal _llm
        if _llm is None:
            _llm = ChatOpenAI(model_name='gpt-4o-mini', streaming=True, openai_api_key=OPENAI_API_KEY)
        return _llm

    async def send() -> None:

        question = text.value
        text.value = ''

        with message_container:
            ui.chat_message(text=question, name='You', sent=True)
            response_message = ui.chat_message(name='Bot', sent=False)
            spinner = ui.spinner(type='dots')

        response = ''
        config = {'callbacks': [NiceGuiLogElementCallbackHandler(log)]}
        async for chunk in get_llm_singleton().astream(question, config=config):
            response += chunk.content
            response_message.clear()
            with response_message:
                ui.html(response)
            await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        message_container.remove(spinner)

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
                .classes('w-full self-center').on('keydown.enter', send)
        ui.markdown('simple chat app built with [NiceGUI](https://nicegui.io)') \
            .classes('text-xs self-end mr-8 m-[-1em] text-primary')
