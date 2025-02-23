from nicegui import ui, app
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from nicegui_start_project.utils import read_html
from . import configs


# todo: 使用模板渲染函数啊，为什么要自己写。比如：jinja2

@app.get(configs.PAGE_PATH, response_class=HTMLResponse)
def countdown_postgraduate_exam(request: Request):
    return read_html(configs.HTML_PATH)


"""
def get_postgraduate_exam_time():
    pass
    
@ui.page(PAGE_PATH)
async def countdown_postgraduate_exam():
    # ### SLAP
    # - 获得今年的考研时间
    # - 获得当前的时间
    # - 计算考研时间与当前时间的差值
    # - 设置定时器，每秒更新面板一次
    pass
"""
