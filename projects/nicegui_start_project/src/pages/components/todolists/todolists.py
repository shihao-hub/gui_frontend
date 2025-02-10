__all__ = ["PAGE_TITLE", "PAGE_PATH"]

from nicegui import ui, app
from fastapi.responses import HTMLResponse

from projects.nicegui_start_project.src.utils import get_random_port, read_html, read_html_head, read_html_body
from projects.nicegui_start_project.src.settings import SOURCE_DIR

PAGE_TITLE = "待办事项"
PAGE_PATH = "/pages/components/todolists"
HTML_PATH = f"{SOURCE_DIR}/pages/components/todolists/todolists.html"


# @app.get("/pages/components/todolists", response_class=HTMLResponse, tags=["todolists"])
# async def todolists():
#     return read_html(HTML_PATH)


@ui.page(PAGE_PATH)
async def todolists():
    # note: ui.page 的 html 有默认设置，因此在这里添加会导致样式存在问题...

    ui.add_head_html(read_html_head(HTML_PATH))
    ui.add_body_html(read_html_body(HTML_PATH))
    # note: 测试发现，add_head_html 和 add_body_html 似乎只适合整个页面全用 html, css, js 开发？
    #       为什么这样说呢？是因为 nicegui 的 ui.label，ui.html 等元素是按顺序插入的。
    #       但是如果在 add_body_html 前面添加 ui.label，那么 ui.label 还是会出现在页面的最下面。这导致了页面布局混乱。


if __name__ == '__main__':
    ui.run(host="localhost", port=get_random_port(10086), reload=False, show=False)
