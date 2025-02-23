"""
### 需求分析
-


### 需求扩展
- 时间追踪工具（如 Toggl Track / RescueTime）：记录时间分配，分析效率盲点。
- AI 助手集成（如 ChatGPT API）：为工具添加智能总结、自动分类或智能回复功能。
  - 出现助手浮动按钮，点击出现浮动窗口，用于问答。

"""
import time

from nicegui import ui

from . import configs


def get_current_ymd():
    return time.strftime("%Y-%m-%d", time.localtime(time.time()))


def get_current_hm():
    return time.strftime("%H:%M", time.localtime(time.time()))


@ui.page(configs.PAGE_PATH, title=configs.PAGE_TITLE)
async def scheduled_notification():
    with ui.row():
        with ui.column():
            date_element = ui.date(value=get_current_ymd(), on_change=lambda e: date_label.set_text(e.value))
            date_label = ui.label()

        with ui.column():
            time_element = ui.time(value=get_current_hm(), on_change=lambda e: time_label.set_text(e.value))
            time_label = ui.label()

        with ui.column():
            async def on_click():
                if date_label.text and time_label.text and event_input.value:
                    ui.notify(f"{date_label.text} {time_label.text}, {event_input.value}")
                    # TODO: 存储到数据库中
                    # Task { time: int, content: str, notify_number: int = 1 }
                    # note: 设计的重要性，在实现某个需求的时候需要进行完整的需求设计、调研等。

            event_input = ui.input()
            event_input.on("keydown.enter", on_click)

            button = ui.button("set notification", on_click=on_click)


if __name__ == '__main__':
    print(get_current_ymd())
    print(get_current_hm())

    pass
