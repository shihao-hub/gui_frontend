"""
### 需求分析
- 英语单词本

### 功能需求
#### 功能需求 1
使用 json.db 文件（实则 json.db.json）持久化数据，由于是文件，参考 redis，可以设置一个定时器，每秒序列化！

该功能使用 mongodb 数据库，文件第一次运行的时候，清空 mongodb，将 json.db 的数据存储到其中，
持久化的时候，将 mongodb 某个数据库数据全部序列化出来（非系统自带数据）

"""

from nicegui import ui

PAGE_TITLE = "单词笔记本"
PAGE_PATH = "/pages/components/word_notebook"


def add_word(container, word):
    with container:
        ui.label(word)


@ui.page(PAGE_PATH)
async def word_notebook():
    with ui.row():
        pass

    words_container = ui.card()

    def iife_words_container_init():
        pass


if __name__ == '__main__':
    pass
