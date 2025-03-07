from loguru import logger

from nicegui import ui

from . import configs


@ui.page(configs.PAGE_PATH, title=configs.PAGE_TITLE)
async def dst_mod_collections():
    ui.add_head_html('''
    <style>
        body {
            background-color: var(--bg-color);
            color: var(--text-color);
        }
    </style>
    ''')

    with ui.column().classes("w-full h-screen"):
        # 导航栏区域
        with ui.row().classes("w-full p-4 bg-gray-100 dark:bg-gray-800 justify-between items-center"):
            with ui.row().classes("items-center gap-4"):
                ui.label("模组集合").classes("text-xl font-bold dark:text-white")
                ui.label("洞穴生态模组").classes("dark:text-white font-medium")  # 新增模组名称标签
            with ui.row().classes("items-center gap-2 ml-auto"):  # 添加ml-auto实现右对齐
                # 暗夜模式状态
                dark_mode = ui.toggle({False: '☀️', True: '🌙'}, value=False)
                dark_mode.bind_value(dark_mode)

        # 主要内容区域
        with ui.row().classes("w-full flex-1 justify-center p-4"):
            # todo: ui.grid, ui.flex?
            with ui.grid(columns=2).classes("gap-4 max-w-4xl"):
                # 示例卡片（后续可替换为动态数据）
                for i in range(6):  # 演示6个卡片
                    # todo: card can be clicked.
                    with ui.card().classes("w-full h-48 p-4 hover:shadow-lg transition-shadow"):
                        ui.label(f"模组 {i + 1}").classes("text-lg font-semibold")
                        ui.separator()
                        ui.label("这里是模组的简要介绍内容，描述模组的主要功能和特色..."
                                 ).classes("text-gray-600 dark:text-gray-300")
                # temp
                with ui.card(), ui.column():
                    with ui.row():
                        ui.label("icon")
                        with ui.column():
                            ui.label("name")
                            ui.label("tags")
                    ui.separator().classes("w-full")  # todo: 熟悉 Tailwind CSS 如何使用
                    ui.label("brief description")

    # 暗夜模式切换逻辑
    async def toggle_dark_mode(e):
        value = e.args[0]
        # logger.info(value)
        css_vars = {
            '--bg-color': '#1a202c' if bool(value) else '#ffffff',
            '--text-color': '#ffffff' if bool(value) else '#1a202c'
        }
        await ui.run_javascript(f"""
            document.documentElement.style.setProperty('--bg-color', '{css_vars['--bg-color']}');
            // document.documentElement.style.setProperty('--text-color', '{css_vars['--text-color']}');
        """)

    dark_mode.on("update:model-value", lambda e: toggle_dark_mode(e))
