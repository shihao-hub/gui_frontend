import os

from nicegui import ui


def read_markdown(relative_filepath):
    static_dir_path = os.path.join(".", "markdowns")
    filepath = os.path.join(static_dir_path, relative_filepath)
    with open(filepath, "r", encoding="utf-8") as file:
        res = file.read()
    return res


with ui.column().classes("h-screen w-full grid grid-rows-8 gap-0"):
    # 顶部导航栏 (1/8)
    with ui.row().classes("row-span-1 bg-blue-100 items-center justify-center"):
        ui.label("导航栏").classes("text-2xl font-bold")

    # 主要内容区 (6/8)
    with ui.row().classes("row-span-6 bg-green-100 p-4"):
        ui.label("内容展示区").classes("text-lg")
        # 这里可以添加其他内容组件
        with ui.card().classes("inline-block w-auto"):
            markdown = ui.markdown(read_markdown("django.txt"))


        def iife_button_one():
            def on_click():
                markdown.content = "Hello, World!"

            ui.button("删除 markdown 元素的内容", on_click=on_click)


        iife_button_one()

        ui.button("点击我")
        ui.button("点击我")

    # 底部 (1/8)
    # with ui.row().classes("row-span-1 bg-red-100 items-center justify-center"):
    #     ui.label("底部信息栏").classes("text-gray-600")

ui.run(host="localhost", port=10086, reload=False, show=False)
