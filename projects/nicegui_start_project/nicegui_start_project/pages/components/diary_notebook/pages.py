from nicegui import ui

from . import configs


@ui.page(configs.PAGE_PATH, title=configs.PAGE_TITLE)
async def diary_notebook():
    pass
