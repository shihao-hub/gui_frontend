from nicegui import ui, app


def iife_one():
    ui.add_head_html("""
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
    
            body {
                font-family: 'Microsoft YaHei', sans-serif;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                background-color: #f5f6fa;
            }
    
            /* 导航栏样式 */
            .navbar {
                background-color: #2c3e50;
                color: white;
                padding: 1rem 2rem;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
    
            .navbar-content {
                max-width: 1200px;
                margin: 0 auto;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
    
            .logo {
                font-size: 1.5rem;
                font-weight: bold;
            }
    
            .nav-links {
                display: flex;
                gap: 2rem;
            }
    
            .nav-links a {
                color: white;
                text-decoration: none;
                transition: color 0.3s;
            }
    
            .nav-links a:hover {
                color: #3498db;
            }
    
            /* 主要内容区样式 */
            .main-content {
                flex: 1;
                display: flex;
                max-width: 1200px;
                margin: 2rem auto;
                gap: 2rem;
                padding: 0 2rem;
            }
    
            .sidebar-left {
                flex: 1;
                background-color: white;
                border-radius: 10px;
                padding: 1rem;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
    
            .content {
                flex: 6;
                background-color: white;
                border-radius: 10px;
                padding: 2rem;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
    
            .sidebar-right {
                flex: 1;
                background-color: white;
                border-radius: 10px;
                padding: 1rem;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
    
            /* 页脚样式 */
            .footer {
                background-color: #2c3e50;
                color: white;
                padding: 2rem;
                margin-top: auto;
            }
    
            .footer-content {
                max-width: 1200px;
                margin: 0 auto;
                text-align: center;
            }
    
            /* 响应式设计 */
            @media (max-width: 768px) {
                .main-content {
                    flex-direction: column;
                    padding: 1rem;
                }
    
                .sidebar-left, .content, .sidebar-right {
                    flex: none;
                    width: 100%;
                }
    
                .nav-links {
                    display: none;
                }
            }
        </style>
    """)

    with ui.element("nav").classes("navbar"):
        with ui.element("div").classes("navbar-content"):
            ui.element("div").classes("logo")
            with ui.element("div").classes("nav-links"):
                ui.link("首页", "#")
                ui.link("关于", "#")
                ui.link("服务", "#")
                ui.link("联系我们", "#")

    with ui.element("div").classes("main-content"):
        pass

    with ui.element("footer").classes("footer"):
        with ui.element("div").classes("footer-content"):
            ui.html(""" <p>&copy; 2024 版权所有</p> """)


def iife_two():
    # 创建选项卡导航栏
    tabs = ui.tabs([
        '主页',
        '产品',
        '关于我们'
    ]).classes('w-full bg-blue-600 text-white')  # 自定义样式

    # 创建对应的内容面板
    with ui.tab_panels(tabs, value='主页').classes('w-full p-4'):
        with ui.tab_panel('主页'):
            ui.label("欢迎访问主页").classes('text-2xl')
        with ui.tab_panel('产品'):
            ui.label("我们的产品列表").classes('text-2xl')
        with ui.tab_panel('关于我们'):
            ui.label("公司简介").classes('text-2xl')


def iife_three():
    # 创建导航栏容器
    with ui.element('nav').classes('bg-gray-800 text-white p-4 flex items-center'):
        # 左侧品牌标识
        with ui.element('div').classes('flex items-center flex-1'):
            with ui.element('span').classes('text-xl font-bold') as span:
                # ui.label('MyApp')
                span.props(""" innerHTML="MyApp" """)

        # 右侧导航菜单
        with ui.element('ul').classes('flex space-x-6'):
            menu_items = [
                ('主页', '#home'),
                ('产品', '#products'),
                ('文档', '#docs'),
                ('联系我们', '#contact')
            ]

            for text, href in menu_items:
                with ui.element('li'):
                    (ui.element('a')
                     .props(f'href={href} innerHTML={text}')
                     .classes('hover:text-blue-300 transition-colors'))

    # 页面内容区域
    with ui.column().classes('p-4'):
        ui.label("页面内容区域").classes('text-2xl')


iife_three()

ui.run(host="localhost", port=10086, reload=False, show=False)
