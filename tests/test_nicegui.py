import tracemalloc
from nicegui import ui
from nicegui.elements.card import Card

from libs.utils import Module
from test_nicegui_elements import *


def main():
    # attention: 此处可以运用设计模式实现顺序执行。
    #            已使用命令模式简单实现

    tracemalloc.start()

    remote_control = RemoteControl()

    # Question: 为什么 with ui.card(): 包裹下面的代码不起作用？创建的元素根本不会放入 card 中。
    # Answer: 因为需要设置作用域，放入函数中可以，但是那个函数的作用域也要属于 card。无语...
    #         这将要求你 ui 和 业务逻辑 要分离！ui 就是 ui，也就是说 ui.x 的操作必须放一块，其他的业务逻辑可以抽出去。

    with ui.card(), ui.row() as root:
        remote_control.add(FlexibilityElement(), root)

    with ui.card(), ui.row().style("gap: 800px;"):
        with ui.column() as child:
            remote_control.add(LabelElement(), child)
            remote_control.add(IconElement(), child)
            remote_control.add(AvatarElement(), child)
            remote_control.add(LinkElement(), child)
            remote_control.add(ButtonElement(), child)
            remote_control.add(BadgeElement(), child)
            remote_control.add(ToggleElement(), child)
            remote_control.add(RadioElement(), child)
        with ui.column() as child:
            remote_control.add(CommonElement(), child)

    remote_control.execute()

    ui.run(host="localhost", port=8890, reload=False, show=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()
