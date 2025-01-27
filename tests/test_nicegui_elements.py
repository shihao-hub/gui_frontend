__all__ = [
    "RemoteControl",
    "FlexibilityElement",
    "LabelElement",
    "IconElement",
    "AvatarElement",
    "LinkElement",
    "ButtonElement",
    "BadgeElement",
    "ToggleElement",
    "RadioElement",
    "CommonElement"
]

from abc import ABC, abstractmethod
from typing import List

from nicegui import ui, app
from libs.utils import Module


def add_hr():
    ui.separator()


class RemoteControl:
    def __init__(self):
        self.commands: List[NiceGuiElement] = []

    def add(self, command):
        self.commands.append(command)

    def execute(self):
        for command in self.commands:
            command.execute()


class NiceGuiElement(ABC):
    @abstractmethod
    def execute(self):
        pass


"""
### Tips
1. 假如英语很好，学习这些东西将太简单了！可惜有一层语言的隔膜，靠翻译学习起来还是太痛苦，甚至不想去学。
2. Python 的 lambda 不好用，我认为这样的话，可以参考 Java 的 lambda 语法。
   
   说实在的，我很想吐槽，Python 因为缩进导致 lambda 功能有限，那为什么不可以添加新的语法实现 lambda 呢？

### 随笔
1. 这个 nicegui 涉及图形库，全是英文的。
- https://fonts.google.com/icons?icon.set=Material+Icons
- https://quasar.dev/vue-components/avatar/
- https://nicegui.io/documentation
2. 感觉 nicegui 的源码挺好的，可以学习下。但是好难啊，至今没尝试过阅读源代码。

   尤其它似乎有属于 Python 的编程风格以及 fastapi 严格的类型注解？
   - __init_subclass__
   - _to_dict
   - @property
   - @classmethod
   - @overload
   - :param type: name of the event (e.g. "click", "mousedown", or "update:model-value")
   - ...
   
   代码写的太牛了！
3. nicegui 基于 fastapi 的，看样子 fastapi 还是值得了解一下的。
   虽然其实 django 真的够用了，但是新技术有新优势。django-ninja 模仿了 fastapi，假如对 fastapi 有了解，那么我对 django-ninja 应该会有更深入的了解。
4. nicegui 源码的 examples 目录下有很多例子，可以参考学习。（学习开源框架）
"""


class FlexibilityElement(NiceGuiElement):
    def execute(self):
        # 变量提升
        text_input = None
        button = None
        result = None

        def on_input():
            button.visible = bool(text_input.value)

        def on_change():
            # on_change 能够触发，但是不知道为什么 button.visible 设置无效
            # print(text_input.value)
            button.visible = bool(text_input.value)

        # 创建一个文本输入框
        text_input = ui.input(label='请输入一些文本', on_change=on_change)
        # text_input = ui.input(label='请输入一些文本', on_change=lambda e: result.set_text('you typed: ' + e.value))
        # result = ui.label()

        # 创建一个按钮，并使其默认不可见
        button = ui.button('提交')
        button.style('display: none;')

        # 使用 bind_visibility_from 方法来绑定按钮的可见性
        button.bind_visibility_from(text_input)
        text_input.on('input', handler=on_input)  # 为什么无法触发事件回调？
        add_hr()


class LabelElement(NiceGuiElement):
    """ 1. 标签 """

    def execute(self):
        ui.label('some label')
        add_hr()


class IconElement(NiceGuiElement):
    """ 2. 图标：此元素基于 Quasar 的 QIcon 组件。[可能的名称参考](https://fonts.google.com/?icon.set=Material+Icons) """

    def execute(self):
        ui.icon('thumb_up', color='primary').classes('text-5xl')
        add_hr()


class AvatarElement(NiceGuiElement):
    """ 3. 头像：一个包装了 Quasar 的 QAvatar 组件的头像元素。[Avatar | Quasar Framework](https://quasar.dev/vue-components/avatar/) """

    def execute(self):
        ui.avatar('favorite_border', text_color='grey-11', square=True)
        ui.avatar('img:https://nicegui.io/logo_square.png', color='blue-2')
        add_hr()


class LinkElement(NiceGuiElement):
    """ 4. 链接 """

    def execute(self):
        ui.link('NiceGUI on GitHub', 'https://github.com/zauberzeug/nicegui')
        add_hr()


class ButtonElement(NiceGuiElement):
    """ 5. 按钮：此元素基于 Quasar 的 QBtn 组件。[Button | Quasar Framework](https://quasar.dev/vue-components/button/) """

    def execute(self):
        ui.button('Click me!', on_click=lambda: ui.notify('You clicked me!'))
        add_hr()


class BadgeElement(NiceGuiElement):
    """ 6. 徽章：一个包装了 Quasar 的 QBadge 组件的徽章元素。。[Badge | Quasar Framework](https://quasar.dev/vue-components/badge/) """

    def execute(self):
        class BadgeModule(Module):
            def run(self):
                # 变量提升
                badge = None

                def on_click():
                    return badge.set_text(f"{int(badge.text) + 1}")

                with ui.button('Click me!', on_click=on_click):
                    badge = ui.badge('0', color='red').props('floating')

        BadgeModule().run()
        add_hr()


class ToggleElement(NiceGuiElement):
    """ 7. 切换：此元素基于 Quasar 的 QBtnToggle 组件。 """

    def execute(self):
        toggle1 = ui.toggle([1, 2, 3], value=1)
        toggle2 = ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(toggle1, 'value')
        add_hr()


class RadioElement(NiceGuiElement):
    """ 8. 单选选择：此元素基于 Quasar 的 QRadio 组件。 """

    def execute(self):
        radio1 = ui.radio([1, 2, 3], value=1).props('inline')
        radio2 = ui.radio({1: 'A', 2: 'B', 3: 'C'}).props('inline').bind_value(radio1, 'value')
        add_hr()


class CommonElement(NiceGuiElement):
    def execute(self):
        # 9. 下拉选择：此元素基于 Quasar 的 QSelect 组件。
        select1 = ui.select([1, 2, 3], value=1)
        select2 = ui.select({1: 'One', 2: 'Two', 3: 'Three'}).bind_value(select1, 'value')
        add_hr()

        # 10. 复选框：此元素基于 Quasar 的 QCheckbox 组件。
        checkbox = ui.checkbox('check me')
        ui.label('Check!').bind_visibility_from(checkbox, 'value')
        add_hr()

        # 11. 开关：此元素基于 Quasar 的 QToggle 组件。
        switch = ui.switch('switch me')
        ui.label('Switch!').bind_visibility_from(switch, 'value')
        add_hr()

        # 12. 滑块：此元素基于 Quasar 的 QSlider 组件。
        slider = ui.slider(min=0, max=100, value=50)
        ui.label().bind_text_from(slider, 'value')
        add_hr()

        # 13. 操纵杆：基于 nipple.js 创建一个操纵杆。[Nipplejs by yoannmoinet](Nipplejs by yoannmoinet)
        ui.joystick(color='blue', size=50,
                    on_move=lambda e: coordinates.set_text(f"{e.x:.3f}, {e.y:.3f}"),
                    on_end=lambda _: coordinates.set_text('0, 0'))
        coordinates = ui.label('0, 0')
        add_hr()

        # 14. 文本输入：此元素基于 Quasar 的 QInput 组件。
        class Input(Module):
            def run(self):
                ui.input(label='Text', placeholder='start typing',
                         on_change=lambda e: result.set_text('you typed: ' + e.value),
                         validation={'Input too long': lambda value: len(value) < 20})
                result = ui.label()
                add_hr()

        Input().run()

        # 15. 文本框：此元素基于 Quasar 的 QInput 组件。
        class TextArea(Module):

            def run(self):
                def on_change(e):
                    print(result)
                    return result.set_text('you typed: ' + e.value)

                ui.textarea(label='Text', placeholder='start typing',
                            on_change=on_change)
                result = ui.label()
                # result = None  # 注意，我认为不应该这样使用闭包... 哪怕这样使用，应该要习惯性模块化。js 中及其容易，py 中相对复杂一些。
                add_hr()

        TextArea().run()

        # 16.
        add_hr()
