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

from nicegui import ui

from .models import Word
from . import configs


def add_word(container, word):
    with container:
        ui.label(word)


@ui.page(configs.PAGE_PATH, title=configs.PAGE_TITLE)
async def word_notebook():
    with ui.row():
        pass

    words_container = ui.card()

    def iife_words_container_init():
        pass


if __name__ == '__main__':
    pass
