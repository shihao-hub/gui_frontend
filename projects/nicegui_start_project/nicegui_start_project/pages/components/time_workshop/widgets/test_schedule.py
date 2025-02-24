from datetime import datetime

from nicegui import ui

TITLE = "倒计时"
ICON = "schedule"


class Widget:
    def __init__(self, parent):
        self._parent = parent

    def init_widget(self):
        with self._parent:
            # 工具2: 倒计时
            with ui.card().tight().classes('p-4'):
                ui.label('重要日期倒计时').classes('text-h6')

                target_date = ui.date(value=datetime.now().strftime('%Y-%m-%d'))
                result = ui.label()

                def update_countdown():
                    # days = (target_date.value - datetime.now()).days
                    days = 1
                    result.text = f"剩余天数：{days} 天" if days >= 0 else f"已过天数：{-days} 天"

                target_date.on('update:modelValue', update_countdown)
                update_countdown()


def init_widget(parent):
    Widget(parent).init_widget()
