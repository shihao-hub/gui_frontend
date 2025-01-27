"""
### Tips
1.

### 随笔
1. 在我看来，nicegui 适合一些非专业人士快速原型开发甚至就是直接实现某个功能。

   对于专业人士来说，纯后端程序员也可以使用这个。如果懂一些前端知识的话，显然没必要用 nicegui 了吧？

   但是，说实在的，nicegui 应该足够支持开发出大部分常用静态网页了吧？
   如果做不到，那就是没有美学思想、没有创新能力等，前端基础元素就那么些，通过他们的组装显然可以实现出很多页面了吧？

   而且 nicegui 前端元素挺多的，还可以嵌入视频呢！（视频好像和图床一样，一个 url 即可！）

   总之，nicegui 是绝对值得了解的！大部分人的网站根本不需要多么高级的功能！
   如果能熟练使用 nicegui，我这个半吊子前端绝对可以做出不错的网站。

   题外话：
   1. 了解原型图设计，参考各种模板，设计出属于自己的网站。
   2. 熟练掌握 nicegui 的基础元素，制作出属于自己的网站。
   3. nicegui + django-ninja 似乎还算适配？
   4. **nicegui 基础元素很多很多**！非常值得了解！文档非常值得学习！
2. 注意，nicegui 使用的是 fastapi 作为 web 服务框架...
   （提到这个，我需要转变思路，要学会在使用中学习，而不是一口气学完再去使用。比如 fastapi... 这个能力也很难训练...）

   而且它的前后端不需要解耦，直接**前后端一把梭** + 可以直接通过 pyinstaller 打包成独立应用。
3. 但是说实在的，**终究是需求驱动开发**。在没有需求摆在面前的情况下，很难训练自己的能力。
   比如：
   - django, django-ninja, nicegui, fastapi, numpy, pandas,
   - html, css, js, vue
   - java web

   工作内容也不过是和业务强相关的牛马工作罢了。
4. gui_frontend 项目应该有自己的虚拟环境。

   怎么说呢，想表达的是，由于第三方库之间可能因为依赖问题导致相互冲突，所以项目如果不需要依赖，就没必要依赖了。

   gui_frontend 和 gui_backend 相互隔离是最佳选择！（微服务思想？）
5. nicegui 是一个轻量级框架，根本没必要用它来做复杂项目，虽然理论上应该是可以的，但是何必为难自己？
6. nicegui 是基于 Vue 的！
7. niceGui 是一个轻量级的 Python 前端框架，旨在简化用户界面的创建。它侧重于提供简单、直观的界面，特别适用于小型项目和快速原型设计。
8.

100. 参考资料
- [python做界面，为什么我会强烈推荐nicegui](https://cloud.tencent.com/developer/article/2321324)
- [如何评价 python 的前端框架 nicegui？](https://www.zhihu.com/question/628191140)
- [NiceGUI 中文版本文档 ](https://github.com/syejing/nicegui-reference-cn)
- [nicegui太香了，跨平台开发和跨平台运行--使用Python+nicegui实现系统布局界面的开发](https://www.cnblogs.com/wuhuacong/p/18463875)
- [工欲善其事，必先利其器-NiceGUI：AI量化投资研究开发](https://zhuanlan.zhihu.com/p/643075836)

"""

from functools import partial

import nicegui
from nicegui import ui
from nicegui_toolkit import inject_layout_tool


def on_submit(input_field, label):
    name = input_field.value
    label.set_text(f"你好, {name}!")


def main():
    # 基于 nicegui 的一个小工具库
    # inject_layout_tool(ide="pycharm", language_locale="zh")

    todolist = ui.input("TODO: 原型设计图")
    todolist = ui.input("TODO: 原型设计图")
    todolist = ui.input("TODO: 原型设计图")
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

    # Question: 为什么 reload=True 的时候，reload 很慢，而且会卡死。
    ui.run(host="localhost", port=8889, reload=False, show=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()
