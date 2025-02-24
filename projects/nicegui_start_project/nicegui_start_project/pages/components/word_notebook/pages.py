"""
### 需求分析
- 英语单词本

### 功能需求
#### 功能需求 1
使用 json.db 文件（实则 json.db.json）持久化数据。
由于是文件，可以参考 redis，设置一个定时器，每秒序列化！

该功能使用 mongodb 数据库，文件第一次运行的时候，清空 mongodb，将 json.db 的数据存储到其中，
持久化的时候，将 mongodb 某个数据库数据全部序列化出来（非系统自带数据）。

但是，目前看来，这个需求并不是太重要。

"""
from typing import Tuple

from nicegui import ui

from .models import Word
from . import configs


def add_word(container, english, chinese):
    with container:
        with ui.row() as row:
            content = ui.label(f"{english} - {chinese}")

            def update_button_on_click():
                with ui.dialog() as dialog, ui.card():
                    english_input, chinese_input = create_input_element()

                    english_input.value = content.text.split("-")[0].strip()
                    chinese_input.value = content.text.split("-")[-1].strip()

                    def ok_button_on_click():
                        if not (english_input.value and chinese_input.value):
                            ui.notify("请输入英文和中文")
                            return

                        content.text = f"{english_input.value} - {chinese_input.value}"
                        content.update()

                        dialog.close()

                    with ui.row():
                        ui.button("OK", on_click=ok_button_on_click)
                        ui.button("CANCEL", on_click=lambda: dialog.close())
                dialog.open()

            update_button = ui.button("UPDATE", on_click=update_button_on_click)
            delete_button = ui.button("DELETE", on_click=lambda: row.delete())


def create_input_element() -> Tuple[ui.input, ui.input]:
    with ui.row():
        ui.label("英文：")
        english_input = ui.input()
    with ui.row():
        ui.label("中文：")
        chinese_input = ui.input()
    return english_input, chinese_input


def add_spacer():
    return ui.html(""" <div style="margin: 0 15px"></div> """)


@ui.page(configs.PAGE_PATH)
async def word_notebook():
    with ui.row():
        with ui.card(), ui.column():
            english_input, chinese_input = create_input_element()

            with ui.row():
                def save_button_on_click():
                    # check if english_input.value and chinese_input.value
                    if not (english_input.value and chinese_input.value):
                        ui.notify("请输入英文和中文")
                        return
                    add_word(words_container, english_input.value, chinese_input.value)

                def clear_button_on_click():
                    english_input.value = ""
                    chinese_input.value = ""

                save_button = ui.button("SAVE", on_click=save_button_on_click)
                clear_button = ui.button("CLEAR", on_click=clear_button_on_click)

        add_spacer()
        add_spacer()
        add_spacer()
        add_spacer()
        add_spacer()

        with ui.card():
            words_container = ui.column()

        def iife_words_container_init():
            # 比如从数据库读取数据
            add_word(words_container, "hello", "你好")

        iife_words_container_init()


if __name__ == '__main__':
    pass
