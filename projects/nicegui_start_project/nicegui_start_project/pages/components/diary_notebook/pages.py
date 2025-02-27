import contextlib
import sqlite3
from pathlib import Path

from nicegui import ui

from . import configs

_connect = sqlite3.connect(f"{Path(__file__).resolve().parent}/diary_notebook.db")
cursor = _connect.cursor()


@contextlib.contextmanager
def connect():
    yield _connect
    _connect.commit()


def iife_create_tables():
    with connect():
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS diaries (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            content TEXT
        );
        """)


iife_create_tables()


@ui.page(configs.PAGE_PATH + "/login", title=configs.PAGE_TITLE)
async def login_or_register():
    def create_diary(user_id):
        title = ui.input('标题').value
        content = ui.textarea('内容').value
        with content():
            cursor.execute('INSERT INTO diaries (user_id, title, content) VALUES (?, ?, ?)', (user_id, title, content))
        ui.notify('日记创建成功')

    def list_diaries(user_id):
        cursor.execute('SELECT * FROM diaries WHERE user_id=?', (user_id,))
        diaries = cursor.fetchall()
        for diary in diaries:
            ui.label(f'{diary[2]} - {diary[3]}')

    def login():
        username = ui.input('用户名').value
        password = ui.input('密码').props('type="password"').value
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        if cursor.fetchone():
            ui.notify('登录成功')
        else:
            ui.notify('用户名或密码错误')

    def register():
        username = ui.input('用户名').value
        password = ui.input('密码').props('type="password"').value
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        if cursor.fetchone():
            ui.notify('用户名已存在，注册失败')
            return
        with connect():
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        ui.notify('注册成功')

    # 登录/注册页面
    ui.button('登录', on_click=login)
    ui.button('注册', on_click=register)


@ui.page(configs.PAGE_PATH, title=configs.PAGE_TITLE)
async def diary_notebook():
    ui.add_head_html('<style>body { background: #f0f2f5; }</style>')

    def create_auth_form():
        """ 创建登录/注册表单组件 """

        # 响应式变量
        login_mode = ui.toggle([True, False], value=True).props('hidden')  # True=登录模式，False=注册模式

        def switch_form(is_login):
            """切换登录/注册表单"""
            login_mode.value = is_login
            # 动态更新按钮样式
            for btn in [login_form, register_form]:
                btn.style(replace=f"background:{'#e8f4ff' if is_login else 'white'}")

        def handle_submit(is_login):
            """处理表单提交"""
            if is_login:
                print(f"登录：{username.value}, {password.value}")
            else:
                if new_password.value != confirm_pwd.value:
                    ui.notify("两次密码不一致！", type='negative')
                    return
                print(f"注册：{new_username.value}, {new_password.value}")

        with ui.card().classes("w-80 p-6 gap-4"):
            # 切换按钮
            with ui.row().classes("w-full justify-between"):
                ui.button("登录", on_click=lambda: switch_form(True)).classes("flex-1")
                ui.button("注册", on_click=lambda: switch_form(False)).classes("flex-1")

            # 动态表单区域
            with ui.column().bind_visibility_from(login_mode, 'value') as login_form:
                username = ui.input("用户名").classes("w-full")
                password = ui.input("密码", password=True).classes("w-full")
                ui.button("登录", on_click=lambda: handle_submit(True)).classes("w-full")

            with ui.column().bind_visibility_from(login_mode, 'value',
                                                  value=lambda v: not v) as register_form:
                new_username = ui.input("新用户名").classes("w-full")
                new_password = ui.input("设置密码", password=True).classes("w-full")
                confirm_pwd = ui.input("确认密码", password=True).classes("w-full")
                ui.button("注册", on_click=lambda: handle_submit(False)).classes("w-full")

            # 底部提示
            ui.separator()
            ui.label("忘记密码？").classes("text-sm text-gray-500 cursor-pointer")

    with ui.column().classes("h-screen items-center justify-center"):
        create_auth_form()
