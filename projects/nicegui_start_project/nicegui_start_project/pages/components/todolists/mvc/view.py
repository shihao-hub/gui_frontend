from typing import List, Optional, Callable, Coroutine, Dict, override

from loguru import logger

from nicegui import ui, app

from nicegui_start_project.utils import Maybe, catch_unhandled_exception
from nicegui_start_project.utils.mvc import View
from ..models import TodoListTypedDict


class TodoListView(View):
    """ 构建界面组件，不处理业务逻辑，仅暴露 UI 元素和事件占位符。 """

    # 在类中声明类型，这样 __init__ 中就不需要了声明并赋值为 None 了，这是 python 某个版本的新特性？
    # 我认为这样的目的是：显示声明这些属性都是不允许为空的！如果没有初始化，直接就会执行 class 没有某个属性！
    task_input: ui.input
    add_button: ui.button
    todo_table: ui.table

    def __init__(self):
        self._error_dialog: Maybe[ui.dialog] = Maybe.empty()

        self._add_todo: Callable[[], Coroutine] = self._placeholder_event

    def set_callbacks(self, *, add_todo: Callable[[], Coroutine]):
        self._add_todo = add_todo

    def build_ui(self) -> None:
        """ 构建界面组件 """
        with ui.column().classes("w-full max-w-4xl mx-auto"):
            with ui.row().classes('w-full no-wrap items-center'):
                self.task_input = ui.input(label="输入新的待办事项").props("outlined").classes("flex-grow")
                self.add_button = ui.button("添加", on_click=lambda: self._add_todo())

            # 个人认为，columns 的元素应该可以和 TypedDict 配合，动态生成这个映射关系！
            # name 是指唯一标识，一般都等于 field
            # note:
            #   columns 中添加了 `"format": self.format_done_column` 直接主页提示：
            #   TypeError: Type is not JSON serializable: method
            #   python 层调用 try except 似乎无法捕获，这个是和 ui.table 有关的，应该是 js 层的错误...
            #   无语啊，这意味着 ui.xxx 传参有问题的时候，似乎没办法直接定位原因啊！
            #   对于这种问题，得出测试代码要经常执行！因为根据测试结果，我们可以缩小范围，更快定位到是哪些新增代码导致的问题！

            # 创建表格
            self.todo_table = ui.table(rows=[]).classes("w-full")
            # 设置分页
            # self.todo_table.pagination = {
            #     "rows_per_page": 10,
            #     "rows_per_page_options": [5, 10, 20],
            #     # "on_pagination_change": on_pagination_change
            # }
            # 定义表格列
            self.todo_table.columns = [
                {"name": "task", "label": "任务名", "field": "task", "align": "center"},
                {"name": "done", "label": "是否完成", "field": "done", "align": "center",
                 # 'cellRenderer': 'html', 'suppressHtmlSanitization': True # 无用... ui.table 没这么自由好像...
                 },
            ]

    def update_table(self, todos: List[TodoListTypedDict]) -> None:
        print(todos)
        self.todo_table.rows = []
        for todo in todos:
            color = "green" if todo.get("done") else "red"
            text = "✅" if todo.get("done") else "❎"
            done_html = f'<span style="color: {color}; cursor: pointer">{text}</span>'
            self.todo_table.rows.append({
                **todo,
                "done": text
            })
        self.todo_table.update()

    def show_error_dialog(self, msg):
        error_msg_label: ui.label = getattr(self.error_dialog, "mount__error_msg_label")
        error_msg_label.text = msg
        self.error_dialog.open()

    @property
    def error_dialog(self) -> ui.dialog:
        if not self._error_dialog.is_present():
            with ui.dialog() as dialog, ui.card().classes("min-w-[200px] min-h-[200px]"):
                error_msg_label = ui.label()
                # 这个好像在 js 里比较常用！
                setattr(dialog, "mount__error_msg_label", error_msg_label)
            self._error_dialog = Maybe.of(dialog)
        return self._error_dialog.get()
