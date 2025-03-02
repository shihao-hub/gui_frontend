import re
from typing import Literal, List

from nicegui import ui, app
from fastapi.responses import HTMLResponse

from nicegui_start_project.utils import get_random_port, read_html_head, read_html_body, read_html
from . import configs
from .mvc import TodoListService, TodoListView, TodoController


# @app.get(configs.PAGE_PATH, response_class=HTMLResponse, tags=["todolists"])
async def todolists():
    """
    实现说明：
        由于 @ui.page 修饰的页面 html 有默认配置，因此在 @ui.page 中调用
        ```python
        ui.add_head_html(read_html_head(HTML_PATH))
        ui.add_body_html(read_html_body(HTML_PATH))
        ```
        会导致样式存在问题...

        而且测试发现，add_head_html 和 add_body_html 似乎只适合整个页面全用 html, css, js 开发？

        为什么这样说呢？是因为 nicegui 的 ui.label，ui.html 等元素是按顺序插入的。

        但是如果在 add_body_html 前面添加 ui.label，那么 ui.label 还是会出现在页面的最下面。这导致了页面布局混乱。
    """
    # question: 单纯一个 html 页面，ui.page 和 app.get 的区别是什么？
    return read_html(configs.HTML_PATH)


@ui.page(configs.PAGE_PATH, title=configs.PAGE_TITLE)
async def todolists():
    # 2025-03-01：
    #   此处属于 MVC 练手，虽然不是那么好，而且我感觉还浪费了时间，但是学习其实应该都是这样的吧？
    #   我自己觉得是浪费了时间，实际上可能我的理解能力就这样？
    #   不要焦虑，请淡定！觉得学的不行大不了之后反复、多次学习就是了！

    TodoController().initialize()
