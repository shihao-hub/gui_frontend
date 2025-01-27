from nicegui import ui

from libs.utils import Module
from tests.test_nicegui_elements import *


def main():
    # attention: 此处可以运用设计模式实现顺序执行。
    #            已使用命令模式简单实现

    remote_control = RemoteControl()

    remote_control.add(FlexibilityElement())
    remote_control.add(LabelElement())
    remote_control.add(IconElement())
    remote_control.add(AvatarElement())
    remote_control.add(LinkElement())
    remote_control.add(ButtonElement())
    remote_control.add(BadgeElement())
    remote_control.add(ToggleElement())
    remote_control.add(RadioElement())
    remote_control.add(CommonElement())

    remote_control.execute()

    ui.run(host="localhost", port=8890, reload=False, show=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()
