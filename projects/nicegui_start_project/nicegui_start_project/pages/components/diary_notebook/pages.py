import contextlib
import sqlite3
import re
from pathlib import Path
from typing import Optional, List

from nicegui import ui

from nicegui_start_project.utils import read_sql
from . import configs

_connect = sqlite3.connect(f"{Path(__file__).resolve().parent}/database/test.db")
cursor = _connect.cursor()


@contextlib.contextmanager
def connect():
    yield _connect
    _connect.commit()


def iife_create_tables():
    with connect():
        cursor.executescript(read_sql(f"{configs.COMPONENT_SOURCE_DIR}/database/scripts/create_tables.sql"))


iife_create_tables()


@ui.page(configs.PAGE_PATH, title=configs.PAGE_TITLE)
async def diary_notebook():
    # todo: 1. SLAP 2. **组合函数模式** 3. 面向对象思想
    # create_left_sidebar()
    # create_main_content()
    # create_right_sidebar()
    # login_or_register()
    # 初始化笔记本数据

    class NoteEntry:
        def __init__(self, title: str, parent: Optional['NoteEntry'] = None):
            self.id = id(self)
            self.title = title
            self.content = "# New Note\nStart writing here..."
            self.parent = parent
            self.children: List['NoteEntry'] = []
            self.expanded = True

    class Notebook:
        def __init__(self):
            self.root = NoteEntry("我的笔记")
            self.current_note: Optional[NoteEntry] = None

    notebook = Notebook()

    def create_tree_node(note: NoteEntry):
        with ui.element('div').classes('ml-4'):
            with ui.row().classes('items-center gap-1'):
                ui.icon('expand_more', size='sm').bind_visibility_from(note, 'expanded')
                ui.icon('chevron_right', size='sm').bind_visibility_from(note, 'expanded', lambda x: not x)
                btn = ui.button(note.title, on_click=lambda: select_note(note))
                btn.classes('text-left justify-start').props('flat')
                ui.button(icon='add', on_click=lambda: create_child(note)).props('flat dense')

            if note.children:
                with ui.element('div').bind_visibility_from(note, 'expanded'):
                    for child in note.children:
                        create_tree_node(child)

    def generate_toc(content: str):
        toc = []
        headers = re.findall(r'^(#{1,3})\s+(.*)', content, re.MULTILINE)
        for level, title in headers:
            indent = 'pl-%d' % (len(level) * 2)
            link = re.sub(r'[^a-zA-Z0-9 ]', '', title).lower().replace(' ', '-')
            toc.append((len(level), title, link))  # 插入元组（Array -> Named Array）
        return toc

    def update_preview():
        """ 更新内容区  """
        notebook.current_note.content = editor.value
        toc_container.clear()
        with toc_container:
            for level, title, link in generate_toc(editor.value):
                ui.link(title, f'#{link}').classes(f'text-sm pl-{level * 4} hover:text-blue-600')

    def create_child(parent: NoteEntry):
        new_note = NoteEntry("New Note", parent)
        parent.children.append(new_note)  # 建立双向关联
        tree_container.clear()
        with tree_container:
            create_tree_node(notebook.root)
        select_note(new_note)

    def select_note(note: NoteEntry):
        # todo: 持久化
        notebook.current_note = note
        editor.value = note.content
        update_preview()

    # 界面布局
    with ui.row().classes('w-full h-screen'):
        # 左侧导航栏
        #   可以封装为 create_left_sidebar()，但是 tree_container 的变量提升的作用就丢失了，不太好吧？
        #   这也体现了 nicegui 的小项目的宿命！
        with ui.column().classes('w-64 bg-gray-100 h-full p-4 border-r'):
            ui.label('Notebooks').classes('text-xl font-bold mb-4')
            with ui.column().classes('w-full') as tree_container:
                create_tree_node(notebook.root)

        # 中间编辑区
        with ui.column().classes('flex-1 p-4 min-w-[600px]'):
            editor = ui.textarea(label='Markdown Editor').classes('w-full h-full')
            editor.on('input', lambda: update_preview())

        # 右侧目录
        with ui.column().classes('w-64 bg-gray-50 h-full p-4 border-l') as toc_container:
            ui.label('Table of Contents').classes('text-lg font-bold mb-4')

    # 初始化选择第一个笔记
    select_note(notebook.root)
