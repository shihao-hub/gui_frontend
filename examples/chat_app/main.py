#!/usr/bin/env python3
from datetime import datetime
from typing import List, Tuple
from uuid import uuid4

from nicegui import ui
from nicegui_toolkit import inject_layout_tool

# QUESTION: (2025.01.30)
#   注意，将该函数移到 utils.py 文件中只是测试，实际上根本不需要。放在当前文件即可，而且还不需要传递 message 参数。
#   为什么该函数移出去后， with ui.x() 中调用仍生效，而不像我自己的代码？
#   目前猜测可能因为运用了命令模式？函数作为参数被传递了？不理解。
from utils import chat_messages, ChatMessages

messages: List[Tuple[str, str, str, str]] = []


@ui.page('/')
async def main():
    # inject_layout_tool()

    # just to test
    cm = ChatMessages()

    user_id = str(uuid4())
    avatar = f'https://robohash.org/{user_id}?bgset=bg2'

    # NOTE: add_css
    ui.add_css(r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}')
    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        def add_input_component():
            with ui.row().classes('w-full no-wrap items-center'):
                with ui.avatar().on('click', lambda: ui.navigate.to(main)):
                    ui.image(avatar)

                def send() -> None:
                    stamp = datetime.now().strftime('%X')
                    messages.append((user_id, avatar, text.value, stamp))
                    text.value = ''
                    # chat_messages.refresh()
                    cm.fn.refresh()

                text = ui.input(placeholder='message') \
                    .on('keydown.enter', send) \
                    .props('rounded outlined input-class=mx-3').classes('flex-grow')

        add_input_component()

        ui.markdown('simple chat app built with [NiceGUI](https://nicegui.io)') \
            .classes('text-xs self-end mr-8 m-[-1em] text-primary')

    await ui.context.client.connected()
    with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
        # chat_messages(messages, user_id)
        cm.fn(messages, user_id)


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(host="localhost", port=11111, reload=False, show=False)
