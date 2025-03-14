import unicodedata
from typing import List, Tuple

from loguru import logger

from nicegui import ui

from nicegui_start_project.utils import read_js
from . import configs
from .configs import UNICODE_CATEGORIES
from .singletons import RefreshNameLabelSingleton


def _get_unicode_chars(start, end) -> List[Tuple[str, str, str]]:
    """生成指定范围内的 Unicode 字符"""
    return [
        (chr(code), f"U+{code:04X}", unicodedata.name(chr(code), "Unknown"))
        for code in range(start, end + 1)
        if unicodedata.category(chr(code)) not in ['Cc', 'Cn']
    ]


def _create_category_cards(category):
    """创建分类卡片"""
    # note: deepseek 的回答，只能说，太美妙了。
    with ui.tab_panel(category):
        with ui.grid(columns='repeat(auto-fill, minmax(200px, 1fr))', rows='auto').classes('w-full gap-4'):
            for chars in UNICODE_CATEGORIES[category]:
                for char, code, name in _get_unicode_chars(*chars):
                    # 添加 nicegui-card 类名
                    # note: tight()
                    with ui.card().tight().classes('nicegui-card p-4 hover:bg-blue-50 transition-all'):
                        with ui.row().classes('items-center gap-4'):
                            ui.label(char).classes('text-4xl w-20')
                            with ui.column():
                                ui.label(code).classes('text-xs font-mono text-gray-600')
                                name_label = ui.label(name).classes('text-sm')
                                RefreshNameLabelSingleton().register_name_labels(name_label, name)


@ui.page(configs.PAGE_PATH, title=configs.PAGE_TITLE)
async def unicode_browser():
    # 页面标题
    ui.markdown("## Unicode 字符浏览器").classes('text-2xl mb-4')

    # 搜索功能
    search = ui.input('搜索', placeholder='输入字符名称或编码...').classes('w-96').props('id=search')

    # 分类标签页
    with ui.tabs().classes('w-full') as tabs:
        for category in UNICODE_CATEGORIES:
            ui.tab(category)

    # 内容面板
    with ui.tab_panels(tabs, value=list(UNICODE_CATEGORIES.keys())[0]).classes('w-full'):
        for category in UNICODE_CATEGORIES:
            _create_category_cards(category)

    # 搜索过滤逻辑
    async def update_search():
        # logger.info("triggering update_search event")
        # todo: 优化 read_js 的使用
        # todo: 推荐改成外部引用的方式，然后 fastapi 挂载静态资源，因为 run_javascript 类似 python eval，不好调试
        await ui.run_javascript(read_js(f"{configs.COMPONENT_SOURCE_DIR}/static/update_search.js"))

    search.on('update:model-value', update_search)

    # page ready?
    RefreshNameLabelSingleton().delay_refresh_name_labels()
