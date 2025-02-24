from datetime import datetime

from nicegui import ui

TITLE = "工作日计算"
ICON = "event"


class Widget:
    def __init__(self, parent):
        self._parent = parent

    def init_widget(self):
        with self._parent:
            # 工具1: 工作日计算
            with ui.card().tight().classes('p-4'):
                ui.label('年度工作日统计').classes('text-h6')

                year_select = ui.select(
                    [str(datetime.now().year - 1), str(datetime.now().year)],
                    value=str(datetime.now().year)
                )

                result_label = ui.label()

                def calculate_workdays():
                    # 这里实现工作日计算逻辑
                    result_label.text = f"{year_select.value}年工作日数：..."

                ui.button('计算', on_click=calculate_workdays)


def init_widget(parent):
    Widget(parent).init_widget()
