import datetime

from nicegui import ui

TITLE = "日期计算"
ICON = "event"


class Widget:
    def __init__(self, parent):
        self.parent = parent

    def init_widget(self):
        def update_result():
            """更新计算结果"""
            selected_date_str = date_picker.value
            try:
                selected_date = datetime.datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            except (TypeError, ValueError):
                return  # 处理无效日期

            today = datetime.date.today()
            delta = selected_date - today
            days = delta.days

            if days > 0:
                result.text = f"距离今天还有 {days} 天"
            elif days < 0:
                result.text = f"已经过去 {-days} 天"
            else:
                result.text = "今天，差0天"

        with self.parent:
            ui.query('body').classes('items-center')
            with ui.column().classes('items-center gap-4 w-full'):
                # 日期选择组件
                date_picker = ui.date(value=datetime.date.today().isoformat())
                # 结果显示标签
                result = ui.label()

                # 监听日期变化事件
                date_picker.on('update:modelValue', update_result)
                # 初始化时计算一次
                update_result()


def init_widget(parent):
    Widget(parent).init_widget()
