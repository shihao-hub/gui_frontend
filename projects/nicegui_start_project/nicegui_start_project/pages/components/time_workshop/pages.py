from datetime import datetime

from nicegui import ui

from . import configs, widgets


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

    # 主页面布局
    with ui.tabs().classes('w-full') as tabs:
        test_event_tab = ui.tab(widgets.test_event.TITLE, icon=widgets.test_event.ICON)
        test_schedule_tab = ui.tab(widgets.test_schedule.TITLE, icon=widgets.test_schedule.ICON)

    with ui.tab_panels(tabs, value=test_event_tab).classes('w-full'):
        with ui.tab_panel(test_event_tab) as tab_panel:
            widgets.test_event.init_widget(tab_panel)

        with ui.tab_panel(test_schedule_tab) as tab_panel:
            widgets.test_schedule.init_widget(tab_panel)
