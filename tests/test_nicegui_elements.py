"""
### TODOLIST
1. 熟练运用 nicegui 开发前端项目（主要是 nicegui 的 ui 挺好看的，半吊子前端前期用它就行了）。
   虽然 nicegui 主要是小型项目，而且应该是前后端不分离一把梭。
   但是最好还是不要用 nicegui 的后端，要学习通用技术！
2. 在将所有样例全部运行之后，必须全部整理一番 key-value，key 是 name，value 是图片！
   后续使用 nicegui 开发时，主要就是 组装框架自带的元素 和 css 调整位置！
3.


### Tips
1. 假如英语很好，学习这些东西将太简单了！可惜有一层语言的隔膜，靠翻译学习起来还是太痛苦，甚至不想去学。
2. Python 的 lambda 不好用，我认为这样的话，可以参考 Java 的 lambda 语法。

   说实在的，我很想吐槽，Python 因为缩进导致 lambda 功能有限，那为什么不可以添加新的语法实现 lambda 呢？
3. 运用提取数据类的重构方法时，有一些体悟，虽然描述不清，但是总的来说就是：实战是很重要的，实战可以让理论发挥用处，
   但是有个问题就是理论总是会遗忘。所以总而言之，学习是痛苦的，人的天赋是有限的。
4. 我总是困惑函数命名要不要加 _ 等等，这些小事。其实很多时候，我只需要快速折中暂时先确定下来就行了，不需要浪费时间。

   因为目前的只是普通水平，有机会阅读其他开源框架的源码学习才行。将时间耗费在这些小事上，就是闭门造车，浪费时间。
5. 学习编程永远都离不开阅读源代码。
   这应该也能算是动态语言的一个优势（读者可以修改源代码而不需要重新编译，以帮助自己理解）

   为什么有这个感想，
   是因为 nicegui 的 ui.refreshable 类源码稍微阅读之后，
   体会到其中的奇技淫巧：

   这个 ui.refreshable 是类，它作为装饰器修饰一个函数后，
   属于是将一个函数封装成了一个类。因此可以额外做很多少事情！
6.

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
5. |2025.01.30| 查看了几个 examples，发现终究还是要学习 html + css 的，尤其 css 设置样式... html 倒是其次。
6. nicegui 的 examples 似乎全是 OPP 思想？
  （说实在的，OPP 思想很正常啊，而且小项目根本不需要 OOP 吧？）

  询问 gpt: 几千到几万才是中项目，而我到目前为止，都没有完整写过多大的项目。。。绝大部分都是学习用的玩具。。。

  TODO: 深入思考 OPP 和 OOP（虽然我认为，需要大量地敲代码才配谈深入思考）
"""

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

import contextlib
import math
import os.path
import pprint
from abc import ABC, abstractmethod
from datetime import datetime
from random import random
from tempfile import SpooledTemporaryFile
from typing import List, Dict, Optional, Callable
from functools import lru_cache

from nicegui import ui, app
from nicegui.element import Element
from nicegui.events import UploadEventArguments, MouseEventArguments

from libs.utils import Module


def add_hr():
    ui.separator()


@contextlib.contextmanager
def _generate_empty_context_element():
    yield


empty_context_element = _generate_empty_context_element()


@lru_cache(maxsize=None)
def read_javascript_code(relative_filepath):
    static_dir_path = os.path.join(".", "javascripts")
    filepath = os.path.join(static_dir_path, relative_filepath)
    with open(filepath, "r", encoding="utf-8") as file:
        res = file.read()
    return res


def read_markdown(relative_filepath):
    static_dir_path = os.path.join(".", "markdowns")
    filepath = os.path.join(static_dir_path, relative_filepath)
    with open(filepath, "r", encoding="utf-8") as file:
        res = file.read()
    return res


def invoke_iife_functions(local_environment: Dict):
    # pprint.pprint(local_environment)
    for k, v in local_environment.items():
        if isinstance(k, str) and k.startswith("iife_") and isinstance(v, Callable):
            v()
        else:
            # print("uncalled: ", k, v)
            ...


class NiceGuiElement(ABC):
    @abstractmethod
    def execute(self, context_element: Element):
        pass


class CommandWrapper:
    def __init__(self,
                 command: NiceGuiElement,
                 context_element: Element = None,
                 ) -> None:
        self.command = command
        self.context_element = context_element or empty_context_element


class RemoteControl:
    def __init__(self):
        self.command_wrappers: List[CommandWrapper] = []

    def add(self, command: NiceGuiElement, context_element: Element = None):
        wrapper = CommandWrapper(command, context_element)
        self.command_wrappers.append(wrapper)

    def execute(self):
        for wrapper in self.command_wrappers:
            wrapper.command.execute(wrapper.context_element)


class FlexibilityElement(NiceGuiElement):
    def execute(self, context_element: Element):
        with context_element:
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

            def iife_test_canvas():
                @ui.page("/test_canvas")
                def page():
                    canvas = ui.element("canvas")
                    canvas.props(""" id="myCanvas" width="500" height="500" style="border:1px solid #000000;" """)

                    async def on_click():
                        await ui.run_javascript(read_javascript_code("test_canvas.js"))

                    button = ui.button("canvas button", on_click=on_click)

            iife_test_canvas()

            add_hr()
            add_hr()
            add_hr()


class LabelElement(NiceGuiElement):
    """ 1. 标签 """

    def execute(self, context_element: Element):
        with context_element:
            ui.label('some label')
            add_hr()


class IconElement(NiceGuiElement):
    """ 2. 图标：此元素基于 Quasar 的 QIcon 组件。[可能的名称参考](https://fonts.google.com/?icon.set=Material+Icons) """

    def execute(self, context_element: Element):
        with context_element:
            ui.icon('thumb_up', color='primary').classes('text-5xl')
            add_hr()


class AvatarElement(NiceGuiElement):
    """ 3. 头像：一个包装了 Quasar 的 QAvatar 组件的头像元素。[Avatar | Quasar Framework](https://quasar.dev/vue-components/avatar/) """

    def execute(self, context_element: Element):
        with context_element:
            ui.avatar('favorite_border', text_color='grey-11', square=True)
            ui.avatar('img:https://nicegui.io/logo_square.png', color='blue-2')
            add_hr()


class LinkElement(NiceGuiElement):
    """ 4. 链接 """

    def execute(self, context_element: Element):
        with context_element:
            ui.link('NiceGUI on GitHub', 'https://github.com/zauberzeug/nicegui')
            add_hr()


class ButtonElement(NiceGuiElement):
    """ 5. 按钮：此元素基于 Quasar 的 QBtn 组件。[Button | Quasar Framework](https://quasar.dev/vue-components/button/) """

    def execute(self, context_element: Element):
        with context_element:
            ui.button('Click me!', on_click=lambda: ui.notify('You clicked me!'))
            add_hr()


class BadgeElement(NiceGuiElement):
    """ 6. 徽章：一个包装了 Quasar 的 QBadge 组件的徽章元素。。[Badge | Quasar Framework](https://quasar.dev/vue-components/badge/) """

    def execute(self, context_element: Element):
        with context_element:
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

    def execute(self, context_element: Element):
        with context_element:
            toggle1 = ui.toggle([1, 2, 3], value=1)
            toggle2 = ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(toggle1, 'value')
            add_hr()


class RadioElement(NiceGuiElement):
    """ 8. 单选选择：此元素基于 Quasar 的 QRadio 组件。 """

    def execute(self, context_element: Element):
        with context_element:
            radio1 = ui.radio([1, 2, 3], value=1).props('inline')
            radio2 = ui.radio({1: 'A', 2: 'B', 3: 'C'}).props('inline').bind_value(radio1, 'value')
            add_hr()


class CommonElement(NiceGuiElement):
    def execute(self, context_element: Element):
        # 9. 下拉选择：此元素基于 Quasar 的 QSelect 组件。
        with context_element:
            def iife_select():
                select1 = ui.select([1, 2, 3], value=1)
                select2 = ui.select({1: 'One', 2: 'Two', 3: 'Three'}).bind_value(select1, 'value')
                add_hr()

            iife_select()

        # 10. 复选框：此元素基于 Quasar 的 QCheckbox 组件。
        with context_element:
            def iife_checkbox():
                checkbox = ui.checkbox('check me')
                ui.label('Check!').bind_visibility_from(checkbox, 'value')
                add_hr()

            iife_checkbox()

        # 11. 开关：此元素基于 Quasar 的 QToggle 组件。
        def iife_switch():
            switch = ui.switch('switch me')
            ui.label('Switch!').bind_visibility_from(switch, 'value')
            add_hr()

        iife_switch()

        # 12. 滑块：此元素基于 Quasar 的 QSlider 组件。
        def iife_slider():
            slider = ui.slider(min=0, max=100, value=50)
            ui.label().bind_text_from(slider, 'value')
            add_hr()

        iife_slider()

        # 13. 操纵杆：基于 nipple.js 创建一个操纵杆。[Nipplejs by yoannmoinet](Nipplejs by yoannmoinet)
        def iife_joystick():
            ui.joystick(color='blue', size=50,
                        on_move=lambda e: coordinates.set_text(f"{e.x:.3f}, {e.y:.3f}"),
                        on_end=lambda _: coordinates.set_text('0, 0'))
            coordinates = ui.label('0, 0')
            add_hr()

        iife_joystick()

        # 14. 文本输入：此元素基于 Quasar 的 QInput 组件。
        def iife_input():
            class Input(Module):
                def run(self):
                    ui.input(label='Text', placeholder='start typing',
                             on_change=lambda e: result.set_text('you typed: ' + e.value),
                             validation={'Input too long': lambda value: len(value) < 20})
                    result = ui.label()
                    add_hr()

            Input().run()

        iife_input()

        # 15. 文本框：此元素基于 Quasar 的 QInput 组件。
        def iife_textarea():
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

        iife_textarea()

        # 16. 数字输入：此元素基于 Quasar 的 QInput 组件。
        def iife_number():
            ui.number(label='Number', value=3.1415927, format='%.2f',
                      on_change=lambda e: result.set_text(f'you entered: {e.value}'))
            result = ui.label()
            add_hr()

        iife_number()

        # 17. 旋钮：此元素基于 Quasar 的 QKnob 组件。该元素用于通过鼠标/触摸滑动从用户获取数字输入。
        def iife_knob():
            knob = ui.knob(0.3, show_value=True)

            with ui.knob(color='orange', track_color='grey-2').bind_value(knob, 'value'):
                ui.icon('volume_up')
            add_hr()

        iife_knob()

        # 18. 颜色输入：此元素扩展了Quasar的QInput组件，具有颜色选择器功能。
        def iife_color_input():
            label = ui.label('Change my color!')
            ui.color_input(label='Color', value='#000000',
                           on_change=lambda e: label.style(f'color:{e.value}'))
            add_hr()

        iife_color_input()

        # 19. 颜色选择器：此元素基于 Quasar 的 QMenu | Quasar Framework和 QColor 组件。
        def iife_color_picker():
            with ui.button(icon='colorize') as button:
                ui.color_picker(on_pick=lambda e: button.style(f'background-color:{e.color}!important'))
            add_hr()

        iife_color_picker()

        # 20. 日期输入：此元素基于 Quasar 的 QDate | Quasar Framework 组件。日期是一个字符串，格式由 mask 参数定义。
        def iife_date():
            ui.date(value='2023-01-01', on_change=lambda e: result.set_text(e.value))
            result = ui.label()
            add_hr()

        iife_date()

        # 21. 时间输入：此元素基于 Quasar 的 QTime 组件QDate | Quasar Framework。时间是一个字符串，格式由 mask 参数定义。
        def iife_time():
            ui.time(value='12:00', on_change=lambda e: result.set_text(e.value))
            result = ui.label()
            add_hr()

        iife_time()

        # 22. 文件上传：基于 Quasar 的 QUploader 组件。
        def iife_upload():
            def on_upload(arguments: UploadEventArguments):
                """
                需求分析：
                接收上传的文件，将其存储起来。
                """
                content = arguments.content
                print(type(content))

                ui.notify(f'Uploaded {arguments.name}')
                print(f"Uploaded file: {arguments.name}")

                # 类似生成器，每次读一行，读完显然会设置 seek
                # count = 0
                # for line in content.readlines():
                #     count += len(line.decode("utf-8"))

                # decoded_content = content.read().decode("utf-8")

                # 分块读取文件内容，联想到 JS 中的大文件上传。
                byte_count = 0
                block = content.read(1024)
                while block:
                    byte_count += len(block)
                    block = content.read(1024)

                print(f"The number of bytes of the file: {byte_count}")  # 打印文件内容

            ui.upload(on_upload=on_upload).classes('max-w-full')
            add_hr()

        iife_upload()

        # 23. 聊天消息：基于 Quasar 的 Chat Message 组件。
        def iife_chat_message():
            ui.chat_message('Hello NiceGUI!',
                            name='Robot',
                            stamp='now',
                            avatar='https://robohash.org/ui')
            add_hr()

        iife_chat_message()

        # 24. 通用元素：这个类是所有其他UI元素的基类。但您可以使用它来创建带有任意 HTML 标签的元素。
        def iife_element():
            with ui.element('div').classes('p-2 bg-blue-100'):
                ui.label('inside a colored div')
            add_hr()

        iife_element()

        def iife_markup_language():
            @ui.page("/markup_language")
            def page():
                # 25. Markdown 元素：将 Markdown 渲染到页面上。
                ui.markdown('''This is **Markdown**.''')
                add_hr()
                # with ui.card():
                #     ui.markdown(read_markdown("django.txt"))
                # add_hr()

                # 26. Mermaid 图表：
                #   用 Markdown 类似的 Mermaid | Diagramming and charting tool 语言编写的图表和图表的渲染。
                #   Mermaid 语法也可以在 Markdown 元素内使用，通过将扩展字符串 'mermaid' 提供给 ui.markdown 元素。
                ui.mermaid('''
                graph LR;
                    A --> B;
                    A --> C;
                ''')
                add_hr()

                """ 27. HTML 元素：
                    将任意的 HTML 渲染到页面上。
                    可以使用 Tailwind Tailwind CSS - Rapidly build modern websites without ever leaving your HTML. 
                    进行样式设置。
                    您还可以使用 ui.add_head_html 将 HTML 代码添加到文档的头部，使用 ui.add_body_html 将其添加到文档的正文部分。
                    
                    HTML 是一种用于创建网页和网页应用程序的标记语言，它定义了网页的结构和内容，包括文本、图像、超链接等。
                """
                ui.html('This is <strong>HTML</strong>.')
                add_hr()

                # 28. SVG：您可以使用 ui.html 元素添加可伸缩矢量图形（Scalable Vector Graphics，SVG）
                svg_content = '''
                    <svg viewBox="0 0 200 200" width="100" height="100" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="100" cy="100" r="78" fill="#ffde34" stroke="black" stroke-width="3" />
                    <circle cx="80" cy="85" r="8" />
                    <circle cx="120" cy="85" r="8" />
                    <path d="m60,120 C75,150 125,150 140,120" style="fill:none; stroke:black; stroke-width:8; stroke-linecap:round" />
                    </svg>'''
                ui.html(svg_content)
                add_hr()

        iife_markup_language()

        def iife_image_audio_video():
            @ui.page("/image_audio_video")
            def page():
                # 29. 图像：显示一幅图片。此元素基于 Quasar 的 QImg 组件。
                ui.image('https://picsum.photos/id/377/640/360')
                add_hr()

                # 30. 标题和叠加：通过在 ui.image 元素内嵌套元素，您可以创建增强效果。
                with ui.image('https://picsum.photos/id/29/640/360'):
                    ui.label('Nice!').classes('absolute-bottom text-subtitle2 text-center')

                with ui.image('https://cdn.stocksnap.io/img-thumbs/960w/airplane-sky_DYPWDEEILG.jpg'):
                    ui.html('''
                        <svg viewBox="0 0 960 638" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="445" cy="300" r="100" fill="none" stroke="red" stroke-width="20" />
                        </svg>
                    ''').classes('bg-transparent')
                add_hr()

                # 31. 交互式图像
                def iife_interactive_image():
                    # TODO: 了解 js 的事件之 mouse 事件。
                    def mouse_handler(e: MouseEventArguments):
                        color = 'SkyBlue' if e.type == 'mousedown' else 'SteelBlue'
                        ii.content += f'<circle cx="{e.image_x}" cy="{e.image_y}" r="15" fill="none" stroke="{color}" stroke-width="4" />'
                        ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')

                    src = 'https://picsum.photos/id/565/640/360'
                    ii = ui.interactive_image(src, on_mouse=mouse_handler, events=['mousedown', 'mouseup'], cross=True)
                    add_hr()

                # 32. 音频：显示一个音频播放器。
                def iife_audio():
                    a = ui.audio('https://cdn.pixabay.com/download/audio/2022/02/22/audio_d1718ab41b.mp3')
                    a.on('ended', lambda _: ui.notify('Audio playback completed'))

                    ui.button(on_click=lambda: a.props('muted'), icon='volume_off').props('outline')
                    ui.button(on_click=lambda: a.props(remove='muted'), icon='volume_up').props('outline')
                    add_hr()

                # 33. 视频：显示一个视频。
                def iife_video():
                    src = 'https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4'
                    v = ui.video(src)
                    v.on('ended', lambda _: ui.notify('Video playback completed'))

                    def on_click_of_volume_off():
                        v.props('volume = 0')
                        ui.run_javascript(f""" alert("volume = {0}") """)

                    def on_click_of_volume_up():
                        v.props('volume = 1')
                        ui.run_javascript(f""" alert("volume = {1}") """)

                    ui.button(on_click=on_click_of_volume_off, icon='volume_off').props('outline')
                    ui.button(on_click=on_click_of_volume_up, icon='volume_up').props('outline')
                    add_hr()

                # 局部测试使用
                invoke_iife_functions(locals())

        iife_image_audio_video()

        def iife_data_elements():
            @ui.page("/data_elements")
            def page():
                # 34.
                def iife_table():
                    columns = [
                        {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True, 'align': 'left'},
                        {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
                    ]
                    rows = [
                        {'name': 'Alice', 'age': 18},
                        {'name': 'Bob', 'age': 21},
                        {'name': 'Carol'},
                    ]
                    ui.table(columns=columns, rows=rows, row_key='name')
                    add_hr()

                # 35. AG Grid (大数据)
                def iife_aggrid():
                    grid = ui.aggrid({
                        'defaultColDef': {'flex': 1},
                        'columnDefs': [
                            {'headerName': 'Name', 'field': 'name'},
                            {'headerName': 'Age', 'field': 'age'},
                            {'headerName': 'Parent', 'field': 'parent', 'hide': True},
                        ],
                        'rowData': [
                            {'name': 'Alice', 'age': 18, 'parent': 'David'},
                            {'name': 'Bob', 'age': 21, 'parent': 'Eve'},
                            {'name': 'Carol', 'age': 42, 'parent': 'Frank'},
                        ],
                        'rowSelection': 'multiple',
                    }).classes('max-h-40')

                    def update():
                        grid.options['rowData'][0]['age'] += 1
                        grid.update()

                    with ui.row():
                        ui.button('Update', on_click=update)

                        # FIXME: 没有这个函数，所以这个文档居然是旧版本？但是哪怕旧版本，为什么要删接口呢...
                        ui.button('Select all', on_click=lambda: grid.call_api_method('selectAll'))
                        ui.button('Show parent',
                                  on_click=lambda: grid.call_column_api_method('setColumnVisible', 'parent', True))
                    add_hr()

                # 36. 图标
                def __iife_chart():
                    # FIXME: 为什么不存在 chart 组件了？
                    chart = ui.chart({
                        'title': False,
                        'chart': {'type': 'bar'},
                        'xAxis': {'categories': ['A', 'B']},
                        'series': [
                            {'name': 'Alpha', 'data': [0.1, 0.2]},
                            {'name': 'Beta', 'data': [0.3, 0.4]},
                        ],
                    }).classes('w-full h-64')

                    def update():
                        chart.options['series'][0]['data'][0] = random()
                        chart.update()

                    with ui.row():
                        ui.button('Update', on_click=update)
                    add_hr()

                # 37. Apache EChart
                def iife_echart():
                    echart = ui.echart({
                        'xAxis': {'type': 'value'},
                        'yAxis': {'type': 'category', 'data': ['A', 'B'], 'inverse': True},
                        'legend': {'textStyle': {'color': 'gray'}},
                        'series': [
                            {'type': 'bar', 'name': 'Alpha', 'data': [0.1, 0.2, 0.3]},
                            {'type': 'bar', 'name': 'Beta', 'data': [0.2, 0.3, 0.4]},
                            {'type': 'bar', 'name': 'Candy', 'data': [0.3, 0.4, 0.5]},
                        ],
                    })

                    def update():
                        echart.options['series'][0]['data'][0] = random() / 2
                        # pprint.pprint(echart.options['series'])
                        echart.update()

                    ui.button('Update', on_click=update)
                    add_hr()

                # 38. Pyplot 上下文：创建一个上下文以配置 Matplotlib 绘图。
                def __iife_pyplot():
                    import numpy as np
                    from matplotlib import pyplot as plt

                    with ui.pyplot(figsize=(3, 2)):
                        x = np.linspace(0.0, 5.0)
                        y = np.cos(2 * np.pi * x) * np.exp(-x)
                        plt.plot(x, y, '-')
                    add_hr()

                # 39. 线性图：使用 pyplot 创建一张线性图。
                def iife_pyplot_line():
                    line_plot = ui.line_plot(n=2, limit=20, figsize=(10, 2), update_every=5) \
                        .with_legend(['sin', 'cos'], loc='upper center', ncol=2)

                    def update_line_plot() -> None:
                        now = datetime.now()
                        x = now.timestamp()
                        y1 = math.sin(x)
                        y2 = math.cos(x)
                        line_plot.push([now], [[y1], [y2]])

                    line_updates = ui.timer(0.1, update_line_plot, active=False)
                    line_checkbox = ui.checkbox('active').bind_value(line_updates, 'active')
                    add_hr()

                # 40. Plotly 元素
                def __iife_plotly():
                    add_hr()

                # 41. 线性进度条：一个包装了 Quasar 的 QLinearProgress 组件的线性进度条。
                def iife_linear_progress():
                    slider = ui.slider(min=0, max=1, step=0.01, value=0.5)
                    ui.linear_progress().bind_value_from(slider, 'value')
                    add_hr()

                # 42. 圆形进度条
                def iife_circular_progress():
                    slider = ui.slider(min=0, max=1, step=0.01, value=0.5)
                    ui.circular_progress().bind_value_from(slider, 'value')
                    add_hr()

                # 43. 旋转器
                def iife_spinner():
                    with ui.row():
                        ui.spinner(size='lg')
                        ui.spinner('audio', size='lg', color='green')
                        ui.spinner('dots', size='lg', color='red')
                    add_hr()

                # 44. 3D 场景
                def iife_scene():
                    with ui.scene().classes('w-full h-64') as scene:
                        scene.sphere().material('#4488ff')
                        scene.cylinder(1, 0.5, 2, 20).material('#ff8800', opacity=0.5).move(-2, 1)
                        scene.extrusion([[0, 0], [0, 1], [1, 0.5]], 0.1).material('#ff8888').move(-2, -2)

                        with scene.group().move(z=2):
                            scene.box().move(x=2)
                            scene.box().move(y=2).rotate(0.25, 0.5, 0.75)
                            scene.box(wireframe=True).material('#888888').move(x=2, y=2)

                        scene.line([-4, 0, 0], [-4, 2, 0]).material('#ff0000')
                        scene.curve([-4, 0, 0], [-4, -1, 0], [-3, -1, 0], [-3, -2, 0]).material('#008800')

                        logo = 'https://avatars.githubusercontent.com/u/2843826'
                        scene.texture(logo, [[[0.5, 2, 0], [2.5, 2, 0]],
                                             [[0.5, 0, 0], [2.5, 0, 0]]]).move(1, -2)

                        teapot = 'https://upload.wikimedia.org/wikipedia/commons/9/93/Utah_teapot_(solid).stl'
                        scene.stl(teapot).scale(0.2).move(-3, 4)

                        scene.text('2D', 'background: rgba(0, 0, 0, 0.2); border-radius: 5px; padding: 5px').move(z=2)
                        scene.text3d('3D', 'background: rgba(0, 0, 0, 0.2); border-radius: 5px; padding: 5px').move(
                            y=-2).scale(.05)
                    add_hr()

                # 45. 树状结构
                def iife_tree():
                    ui.tree([
                        {'id': 'numbers', 'children': [{'id': '1', "children": [{"id": "11"}]}, {'id': '2'}]},
                        {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
                    ], label_key='id', on_select=lambda e: ui.notify(e.value))
                    add_hr()

                # 46. 日志视图
                def iife_log():
                    def on_click():
                        log.push(datetime.now().strftime('%X.%f')[:-5])

                    log = ui.log(max_lines=10).classes('w-full h-20')
                    ui.button('Log time', on_click=on_click)
                    add_hr()

                # 47. 编辑器
                def iife_editor():
                    editor = ui.editor(placeholder='Type something here')
                    # TODO: 让这个 v 换行
                    ui.markdown().bind_content_from(editor, 'value',
                                                    backward=lambda v: f'HTML code:\n```\n{v}\n```')
                    add_hr()

                # 48. 代码
                def iife_code():
                    ui.code('''
                        from nicegui import ui

                        ui.label('Code inception!')

                        ui.run()
                    ''').classes('w-full')
                    add_hr()

                # 49. JSON编辑器
                def iife_json_editor():
                    json_data = {
                        'array': [1, 2, 3],
                        'boolean': True,
                        'color': '#82b92c',
                        None: None,
                        'number': 123,
                        'object': {
                            'a': 'b',
                            'c': 'd',
                        },
                        'time': 1575599819000,
                        'string': 'Hello World',
                    }
                    ui.json_editor({'content': {'json': json_data}},
                                   on_select=lambda e: ui.notify(f'Select'),
                                   on_change=lambda e: ui.notify(f'Change'))
                    add_hr()

                invoke_iife_functions(locals())

        iife_data_elements()

        def iife_layout():
            @ui.page('/layout')
            def page():
                # 50. 卡片：此元素基于 Quasar 的 QCard 组件 Card | Quasar Framework。它提供了一个带有投影阴影的容器。
                #     注意：Quasar 组件和此元素之间有细微差异。与此元素不同，原始的 QCard 默认没有填充，并隐藏了嵌套元素的外边框。
                #     如果您想要原始的行为，请使用 tight 方法。如果您希望子元素有填充和边框，请将子元素放入另一个容器中。
                def iife_card():
                    with ui.card().tight():
                        ui.image('https://picsum.photos/id/684/640/360')
                        with ui.card_section():
                            ui.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...')
                    add_hr()

                # 51. 列元素：提供一个容器，按列排列其子元素。
                def iife_column():
                    with ui.column():
                        ui.label('label 1')
                        ui.label('label 2')
                        ui.label('label 3')
                    add_hr()

                # 52. 行元素：提供一个容器，按行排列其子元素。
                def iife_row():
                    with ui.row():
                        ui.label('label 1')
                        ui.label('label 2')
                        ui.label('label 3')
                    add_hr()

                # 53. 网格元素：提供一个容器，以网格形式排列其子元素。
                def iife_grid():
                    with ui.grid(columns=2):
                        ui.label('Name:')
                        ui.label('Tom')

                        ui.label('Age:')
                        ui.label('42')

                        ui.label('Height:')
                        ui.label('1.80m')
                    add_hr()

                # 54. 清除容器内容
                def iife_remove_container_contents():
                    container = ui.row()

                    count = 0

                    def add_face():
                        nonlocal count

                        with container:
                            count += 1
                            with ui.column():
                                ui.icon(f'face')
                                ui.label(f'{count}')

                    add_face()

                    ui.button('Add', on_click=add_face)

                    def on_click_of_remove():
                        # Question: 为什么 container.slots 返回值和 __iter__ 函数里面对不上？奇怪。
                        # pprint.pprint([slot for slot in container.slots.values()])  # 默认有个 default 键
                        # pprint.pprint(list(container))
                        if list(container):
                            container.remove(0)

                    ui.button('Remove', on_click=on_click_of_remove)
                    ui.button('Clear', on_click=container.clear)
                    add_hr()

                # 55. 展开元素：提供一个可展开的容器，基于 Quasar 的 QExpansionItem 组件。Expansion Item | Quasar Framework
                def iife_expansion():
                    with ui.expansion('Expand!', icon='work').classes('w-full'):
                        ui.label('inside the expansion')
                    add_hr()

                # 56. 滚动区域：通过封装内容以自定义滚动条的方式。
                def iife_scroll_area():
                    with ui.row():
                        with ui.card().classes('w-32 h-32'):
                            with ui.scroll_area():
                                ui.label('I scroll. ' * 20)
                        with ui.card().classes('w-32 h-32'):
                            ui.label('I will not scroll. ' * 10)

                add_hr()

                # 57. 分隔符：
                #    此元素基于 Quasar 的 QSeparator 组件。Separator | Quasar Framework
                #    它用作卡片、菜单和其他组件容器的分隔符，类似于HTML的标签。
                def iife_separator():
                    ui.label('text above')
                    ui.separator()
                    ui.label('text below')
                    add_hr()

                # 58. 分割器：ui.splitter 元素将屏幕空间分为可调整大小的部分，允许您在应用程序中创建灵活且响应式的布局。
                #     它提供了三个可自定义的插槽，before、after 和 separator，可用于在分割器内嵌入其他元素。
                def iife_splitter():
                    with ui.splitter() as splitter:
                        with splitter.before:
                            ui.label('This is some content on the left hand side.').classes('mr-2')
                        with splitter.after:
                            ui.label('This is some content on the right hand side.').classes('ml-2')
                    add_hr()

                # 59. 标签页：ui.tabs 创建了标签页的容器，
                #     例如，可以放置在 ui.header 中。ui.tab_panels 创建了用于标签面板的容器，
                #     其中包含实际内容。每个 ui.tab_panel 与一个 ui.tab 元素相关联。
                def iife_tabs():
                    with ui.tabs().classes('w-full') as tabs:
                        one = ui.tab('One')
                        two = ui.tab('Two')

                    with ui.tab_panels(tabs, value=two).classes('w-full'):
                        with ui.tab_panel(one):
                            ui.label('First tab')
                            # ui.timer(1, lambda: ui.notify('First tab'))

                        with ui.tab_panel(two):
                            ui.label('Second tab')
                            # ui.timer(1, lambda: ui.notify('Second tab'))

                    add_hr()

                # 60. 步进器
                #     为了避免在切换步骤时出现动态元素的问题，此元素使用了 Vue 的 keep-alive 组件。
                #     如果客户端性能成为问题，可以禁用此功能。
                def iife_stepper():
                    with ui.stepper().props('vertical').classes('w-full') as stepper:
                        with ui.step('Preheat'):
                            ui.label('Preheat the oven to 350 degrees')
                            with ui.stepper_navigation():
                                ui.button('Next', on_click=stepper.next)
                        with ui.step('Ingredients'):
                            ui.label('Mix the ingredients')
                            with ui.stepper_navigation():
                                ui.button('Next', on_click=stepper.next)
                                ui.button('Back', on_click=stepper.previous).props('flat')
                        with ui.step('Bake'):
                            ui.label('Bake for 20 minutes')
                            with ui.stepper_navigation():
                                ui.button('Done', on_click=lambda: ui.notify('Yay!', type='positive'))
                                ui.button('Back', on_click=stepper.previous).props('flat')
                    add_hr()

                # 61. 时间线
                def iife_timeline():
                    with ui.timeline(side='right'):
                        ui.timeline_entry('Rodja and Falko start working on NiceGUI.',
                                          title='Initial commit',
                                          subtitle='May 07, 2021')
                        ui.timeline_entry('The first PyPI package is released.',
                                          title='Release of 0.1',
                                          subtitle='May 14, 2021')
                        ui.timeline_entry('Large parts are rewritten to remove JustPy '
                                          'and to upgrade to Vue 3 and Quasar 2.',
                                          title='Release of 1.0',
                                          subtitle='December 15, 2022',
                                          icon='rocket')
                    add_hr()

                # 62. 走马灯
                #     此元素代表了 Quasar 的 QCarousel 组件 Carousel | Quasar Framework。它包含个别的走马灯幻灯片。
                def iife_carousel():
                    with ui.carousel(animated=True, arrows=True, navigation=True).props('height=180px'):
                        with ui.carousel_slide().classes('p-0'):
                            ui.image('https://picsum.photos/id/30/270/180').classes('w-[270px]')
                        with ui.carousel_slide().classes('p-0'):
                            ui.image('https://picsum.photos/id/31/270/180').classes('w-[270px]')
                        with ui.carousel_slide().classes('p-0'):
                            ui.image('https://picsum.photos/id/32/270/180').classes('w-[270px]')
                    add_hr()

                # 63. 菜单
                #     基于 Quasar 的 QMenu 组件 QMenu | Quasar Framework 创建菜单。菜单应放置在应该显示的元素内部。
                def iife_menu():
                    with ui.row().classes('w-full items-center'):
                        result = ui.label().classes('mr-auto')
                        with ui.button(icon='menu'):
                            with ui.menu() as menu:
                                ui.menu_item('Menu item 1', lambda: result.set_text('Selected item 1'))
                                ui.menu_item('Menu item 2', lambda: result.set_text('Selected item 2'))
                                ui.menu_item('Menu item 3 (keep open)',
                                             lambda: result.set_text('Selected item 3'), auto_close=False)
                                ui.separator()
                                ui.menu_item('Close', on_click=menu.close)
                    add_hr()

                # 64. 工具提示
                def iife_tooltip():
                    ui.label('Tooltips...').tooltip('...are shown on mouse over')
                    with ui.button(icon='thumb_up'):
                        ui.tooltip('I like this').classes('bg-green')
                    add_hr()

                # 65. 通知：在屏幕上显示通知。注意：您可以根据 Quasar 的 Notify | Quasar Framework API 传递附加的关键字参数。
                ui.button('Say hi!', on_click=lambda: ui.notify('Hi!', close_button='OK'))
                add_hr()

                # 66. 对话框
                #     基于 Quasar 的 QDialog 组件 Dialog | Quasar Framework 创建对话框。
                #     默认情况下，单击或按 ESC 键即可关闭它。要使其保持可见，可以在对话框元素上设置 .props('persistent')。
                def iife_dialog():
                    # ui.column().style(""" background: white; outline: true;  """):
                    with ui.dialog() as dialog, ui.card():
                        ui.label('Hello world!')
                        ui.button('Close', on_click=dialog.close)

                    ui.button('Open a dialog', on_click=dialog.open)
                    add_hr()

                invoke_iife_functions(locals())

        iife_layout()

        def iife_facade():
            @ui.page('/facade')
            def page():
                # 67.
                add_hr()

                # 68.
                add_hr()

                # 69.
                add_hr()

                # 70.
                add_hr()

                # 71.
                add_hr()

                # 72.
                add_hr()

                invoke_iife_functions(locals())

        iife_facade()
