import os

from nicegui import ui, app


# 配置静态文件路由
@app.get("/static/{file}")
def serve_static(file: str):
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    return app.send_file(os.path.join(static_dir, file))


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

ui.add_body_html("""
    <!-- 导航栏 -->
    <nav class="navbar">
        <div class="navbar-content">
            <div class="logo">Logo</div>
            <div class="nav-links">
                <a href="#">首页</a>
                <a href="#">关于</a>
                <a href="#">服务</a>
                <a href="#">联系我们</a>
            </div>
        </div>
    </nav>

    <!-- 主要内容区 -->
    <div class="main-content">
        <!-- 左侧边栏 -->
        <aside class="sidebar-left">
            <h3>左侧栏</h3>
            <ul>
                <li>菜单项 1</li>
                <li>菜单项 2</li>
                <li>菜单项 3</li>
            </ul>
        </aside>

        <!-- 中间内容区 -->
        <main class="content">
            <h2>主要内容区</h2>
            <p>这里是主要内容区域，占据页面的大部分空间。</p>
            <p>你可以在这里放置文章、图片等主要内容。</p>
        </main>

        <!-- 右侧边栏 -->
        <aside class="sidebar-right">
            <h3>右侧栏</h3>
            <ul>
                <li>推荐 1</li>
                <li>推荐 2</li>
                <li>推荐 3</li>
            </ul>
        </aside>
    </div>

    <!-- 页脚 -->
    <footer class="footer">
        <div class="footer-content">
            <p>&copy; 2024 版权所有</p>
        </div>
    </footer>
""")


ui.run(host="localhost", port=10086, reload=False, show=False)
