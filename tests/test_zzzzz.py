import threading
import time

from nicegui import ui


# TODO: 线程池
# NOTE: 其实代码不管写得再乱，如果它的体量较小。比如组件库，每个组件都是一个小模块，那么代码乱不乱无所谓的！

def set_timeout(cb, delay):
    def target():
        time.sleep(delay)
        cb()

    thread = threading.Thread(target=target)
    thread.start()


def open_dialog():
    label.set_text("call open_dialog")

    def cb():
        label.set_text("reset")

    set_timeout(cb, 2)

    # 创建一个对话框
    with ui.dialog() as dialog, ui.card():
        ui.label('请输入您的名字:')
        user_input = ui.input(placeholder='姓名')  # 输入框

        with ui.row():
            ui.button('确认', on_click=lambda: handle_input(user_input.value, dialog))
            ui.button('取消', on_click=dialog.close)  # 关闭对话框的按钮
    dialog.open()


def handle_input(user_name, dialog):
    print(user_name)
    dialog.close()
    with main_window:
        ui.label(f'您输入的名字是: {user_name}')


main_window = ui.card()

with main_window:
    button = ui.button('打开输入框', on_click=open_dialog)  # 主界面的按钮
    label = ui.label("")

ui.run(host="localhost", port=10086, reload=False, show=False)
