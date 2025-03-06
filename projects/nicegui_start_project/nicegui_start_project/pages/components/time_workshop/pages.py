import collections
import importlib
import os
from datetime import datetime
from pathlib import Path
from typing import List

from loguru import logger

from nicegui import ui

from nicegui_start_project.settings import SOURCE_DIR
from . import configs

CURRENT_PATH = str(Path(__file__).resolve().parent)


@ui.page(configs.PAGE_PATH, title=configs.PAGE_TITLE)
async def time_workshop():
    """

    ### ui.tabs, ui.tab, ui.tab_panels, ui.tab_panel
    1. ui.tabs()：创建横向排列的导航栏（类似浏览器标签栏）。
       - value：当前选中标签的绑定变量。该参数决定初始默认显示哪个工具的面板。
       - on_change：切换标签时的回调函数
    2. ui.tab()：在选项卡容器中添加一个可点击的按钮。
       - 文字标签（必填）
       - 图标（通过icon参数使用Quasar图标库）
       - 禁用状态（disable=True）
    3. ui.tab_panels()：作为所有内容面板的容器，与 tabs 容器关联，确保点击标签时切换对应的内容。
       - tabs：要关联的选项卡容器
       - value：初始显示的面板（通常绑定到第一个ui.tab()）
    4. ui.tab_panel()：每个内容面板，包含特定工具的实际 UI 组件，比如输入框、按钮和结果展示区域。
       - 必须与一个 ui.tab() 对应
       - 内部可以包含任意复杂的内容布局
       - 当对应标签被点击时自动显示
    """

    # note: 约定大于配置！

    # 注意，Js 存在变量提升多半是因为 js 是单线程的。
    # Python 有类似的变量提升效果，但是 Python 并非单线程呀？
    # 可是虽然 Python 不是单线程，但是只要保证线程执行的函数并未使用 nonlocal 变量，应该没问题吧？

    def get_modules():
        res = []
        for name in os.listdir(f"{CURRENT_PATH}/tab_widgets"):
            # 忽略 _ 和 . 前缀、忽略文件夹
            if (name.startswith("_")
                    or name.startswith(".")
                    or os.path.isdir(f"{CURRENT_PATH}/tab_widgets/{name}")):
                continue

            try:
                name_with_no_ext = os.path.splitext(name)[0]
                module = importlib.import_module(f"{configs.PACKAGE_PATH}.tab_widgets.{name_with_no_ext}")
                res.append(module)
            except ImportError as e:
                logger.error(f"{e}")
        return res

    # todo: 不要用导航栏，可以用侧边栏！

    UiTabsElement = collections.namedtuple("ui_tabs_element", ["module", "tab"])
    ui_tabs: List[UiTabsElement] = []

    # 主页面布局
    with ui.tabs().classes('w-full') as tabs:
        for module in get_modules():
            tab = ui.tab(module.TITLE, icon=module.ICON)
            ui_tabs_element = UiTabsElement(module, tab)
            # print("tab parent: ", tab.parent)
            ui_tabs.append(ui_tabs_element)

    # 选项卡面板
    with ui.tab_panels(tabs).classes('w-full'):
        for elem in ui_tabs:
            with ui.tab_panel(elem.tab) as tab_panel:
                elem.module.init_widget(tab_panel)

    # create_menu
    result = ui.label().classes('mr-auto')
    with ui.button(icon="menu"):
        with ui.menu() as menu:
            ui.menu_item('Menu item 1', lambda: result.set_text('Selected item 1'))
            ui.menu_item('Menu item 2', lambda: result.set_text('Selected item 2'))
            ui.menu_item('Menu item 3 (keep open)',
                         lambda: result.set_text('Selected item 3'), auto_close=False)
            ui.separator()
            ui.menu_item('Close', on_click=menu.close)
