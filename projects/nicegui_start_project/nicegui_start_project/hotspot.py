"""
### 需求分析
通过形如 python hotspot.py xxx 的方式进行启动热点分析？

初步构想：
- python hotspot.py 启动一个页面，调用接口展示热点数据
- 主项目在编写代码时，进行埋点操作，并提供对外路由以供 hotspot.py 调用，
  推荐练习一下权限校验，给 hotspot.py 提供一个唯一 token 等，仅供其调用
- 关于埋点操作，目前初步设想如下：
  - 能够记录埋点的执行位置
  - 能够记录某段代码的执行时间

题外话，推荐寻找第三方热点分析库，这些多半可以从底层 CPython 的层面进行热点分析！

"""

from nicegui import ui


@ui.page("/", title="Hotspot Analysis")
def main():
    pass


if __name__ == '__main__':
    ui.run(host="localhost", port=12100, reload=False, show=False, favicon="🔥")
