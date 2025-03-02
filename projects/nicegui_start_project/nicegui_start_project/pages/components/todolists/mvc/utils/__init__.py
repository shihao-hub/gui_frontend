import abc
from typing import Generic, TypeVar, override, List, Callable, Coroutine, Dict

from loguru import logger
from nicegui import ui

S = TypeVar("S", bound="Service")
V = TypeVar("V", bound="View")


def show_error_dialog(error_msg):
    dialog = ui.dialog().classes("w-96")
    with dialog, ui.card().classes("w-full p-6 rounded-lg shadow-lg"):
        ui.label("❌ 错误").classes("text-2xl font-bold text-red-600 mb-4")
        ui.label(f"{error_msg}").classes("text-gray-700 text-center mb-4")
    dialog.open()


class Service(abc.ABC):
    pass


class View(abc.ABC):

    def _placeholder_event(self, *args, **kwargs):
        """ 占位事件 """
        this = self
        logger.warning("存在未被初始化的事件")

    @abc.abstractmethod
    def build_ui(self) -> None:
        """ 初始化视图/构建界面组件 """

    @abc.abstractmethod
    def set_callbacks(self, **callbacks: List[Callable[[...], Coroutine]]):
        """ 设置回调，Controller 设置给 View """

    @staticmethod
    def show_error_dialog(error_msg):
        return show_error_dialog(error_msg)


class Controller(abc.ABC, Generic[S, V]):
    service: S
    view: V

    def __init__(self, service: S, view: V):
        self.service = service
        self.view = view
        self._initialized = False  # protected

    def initialize(self):
        """ 延迟初始化： """
        if self._initialized:
            return

        assert self.service is not None
        assert self.view is not None

        self.view.build_ui()
        self._bind_events()
        self._refresh_view()

        _initialized = True

    @abc.abstractmethod
    def _bind_events(self) -> None:
        """ 绑定事件逻辑/事件处理器 """

    @abc.abstractmethod
    def _refresh_view(self) -> None:
        """ 初始数据加载 """
