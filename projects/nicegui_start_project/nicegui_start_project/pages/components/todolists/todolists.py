import re
from typing import Literal

from nicegui import ui, app
from fastapi.responses import HTMLResponse

from nicegui_start_project.settings import SOURCE_DIR
from nicegui_start_project.utils import get_random_port

# constants
PAGE_TITLE = "待办事项"
PAGE_PATH = "/pages/components/todolists"
HTML_PATH = f"{SOURCE_DIR}/pages/components/todolists/todolists.html"


# question: 单纯一个 html 页面，ui.page 和 app.get 的区别是什么？


# todo: cache 对接 redis（当然，还需要遵循 如非必要，勿增实体 的原则）
# note: 注释掉的话，html 就可以视为配置文件了，刷新而不需要重启就可以更新 html 内容！
# @functools.cache
def read_html(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def _read_html_tag(filename: str, tag_name: Literal["head", "body"]) -> str:
    content = read_html(filename)
    pattern = re.compile(rf"<{tag_name}>(.*?)</{tag_name}>", re.DOTALL)
    match = pattern.search(content)
    assert match is not None
    return match.group(1)


def read_html_head(filename: str) -> str:
    return _read_html_tag(filename, "head")


def read_html_body(filename: str) -> str:
    return _read_html_tag(filename, "body")


@app.get("/pages/components/todolists", response_class=HTMLResponse, tags=["todolists"])
async def todolists():
    return read_html(HTML_PATH)


"""
@ui.page(PAGE_PATH)
async def todolists():
    # note: ui.page 的 html 有默认设置，因此在这里添加会导致样式存在问题...

    ui.add_head_html(read_html_head(HTML_PATH))
    ui.add_body_html(read_html_body(HTML_PATH))
    # note: 测试发现，add_head_html 和 add_body_html 似乎只适合整个页面全用 html, css, js 开发？
    #       为什么这样说呢？是因为 nicegui 的 ui.label，ui.html 等元素是按顺序插入的。
    #       但是如果在 add_body_html 前面添加 ui.label，那么 ui.label 还是会出现在页面的最下面。这导致了页面布局混乱。

"""

if __name__ == '__main__':
    ui.run(host="localhost", port=get_random_port(10086), reload=False, show=False)
