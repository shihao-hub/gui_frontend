from functools import partial

import nicegui
from nicegui import ui
from nicegui_toolkit import inject_layout_tool


def on_submit(input_field, label):
    name = input_field.value
    label.set_text(f"你好, {name}!")


def main():
    inject_layout_tool(ide="pycharm", language_locale="zh")

    input_field = ui.input("请输入你的名字")
    label = ui.label("欢迎使用 NiceGUI!")

    # on_submit 无法移到 main 函数外面，因为需要闭包... 这看起来太奇怪了...
    # def on_submit():
    #     name = input_field.value
    #     label.set_text(f"你好, {name}!")

    ui.button("提交", on_click=partial(on_submit, input_field, label))

    with ui.card(), ui.row():
        ui.avatar("home")

        with ui.column():
            with ui.row():
                ui.label("数据大宇宙")
                ui.icon("mail")
                ui.label("发消息")

            with ui.row():
                ui.button("充电")
                ui.button("+ 关注 670")

    ui.run(host="localhost", port=8889, reload=False, show=False)


main()
