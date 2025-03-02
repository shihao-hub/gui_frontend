import traceback
from typing import override, Type

from loguru import logger

from nicegui import ui
from nicegui.events import TableSelectionEventArguments

from nicegui_start_project.utils import catch_unhandled_exception
from .service import TodoListService
from .view import TodoListView
from .utils import Controller, show_error_dialog


class TodoController(Controller[TodoListService, TodoListView]):
    """
    绑定事件逻辑，协调模型层和视图层。

    Controller 管理交互

    职责：
    - 接收用户输入：
      - Controller 是用户输入的处理层，负责接收来自 View 的用户请求（如点击按钮、提交表单）。
    - 协调 Model 和 View：
      - Controller 调用 Model 处理业务逻辑，并根据处理结果更新 View。
      - 例如，用户登录时，Controller 将用户名和密码传递给 Model 验证，并根据验证结果跳转到成功页面或显示错误提示。
    - 流程控制：
      - Controller 负责应用程序的流程控制，决定下一步的操作（如页面跳转、数据刷新）。

    特点
    - 无业务逻辑：Controller 不包含核心业务逻辑，只负责协调 Model 和 View。
    - 无数据存储：Controller 不直接操作数据，所有数据操作都通过 Model 完成。
    - 轻量级：Controller 的代码通常比较简单，专注于流程控制。
    """

    def __init__(self):
        super().__init__(TodoListService(), TodoListView())

    def _bind_events(self) -> None:
        self.view.set_callbacks(add_todo=self._add_task)

    def _refresh_view(self) -> None:
        self.view.update_table(self.service.get_todos())

    @catch_unhandled_exception
    async def _add_task(self):
        try:
            task = self.view.task_input.value
            self.service1.add_todo(task)
            self.view.task_input.value = ""  # 清空输入框
            self._refresh_view()
        except Exception as e:
            logger.error(f"{e}\n{traceback.format_exc()}")

    @catch_unhandled_exception
    async def _toggle_task_done(self, event: TableSelectionEventArguments, done: ui.html):
        print(event)
        uid = getattr(done, "mount__uid")
        self.service.toggle_done(uid)
        self._refresh_view()
