from typing import List, Tuple

from nicegui import ui


@ui.refreshable
def chat_messages(messages: List[Tuple[str, str, str, str]], own_id: str) -> None:
    if messages:
        for user_id, avatar, text, stamp in messages:
            ui.chat_message(text=text, stamp=stamp, avatar=avatar, sent=own_id == user_id)
    else:
        ui.label('No messages yet').classes('mx-auto my-36')
    ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')


class ChatMessages:
    @ui.refreshable
    def fn(self, messages: List[Tuple[str, str, str, str]], own_id: str) -> None:
        if messages:
            for user_id, avatar, text, stamp in messages:
                ui.chat_message(text=text, stamp=stamp, avatar=avatar, sent=own_id == user_id)
        else:
            ui.label('No messages yet').classes('mx-auto my-36')
        ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
