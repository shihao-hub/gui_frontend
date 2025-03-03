from nicegui import ui

from . import configs


@ui.page(configs.PAGE_PATH, title=configs.PAGE_TITLE)
async def website_collections():
    for website in configs.WEBSITES:
        with ui.card().style("width: 300px; margin: 10px; padding: 10px; border-radius: 10px;"):
            with ui.row():
                if website.icon:
                    ui.icon(website.icon, size="50px")
                with ui.column():
                    def _repeat_blank(num=0):
                        return "&nbsp;" * num

                    ui.label("网站名：  " + website.name)
                    if website.description:
                        ui.label("网页描述：" + website.description)
                    ui.label("收藏目的：" + website.purpose)
                    with ui.row().classes("justify-end ml-auto"):  # 起作用的是 ml-auto，它表示左侧自动边距，将链接推到右侧
                        ui.link("点击进入", website.url).props('target="_blank"')
