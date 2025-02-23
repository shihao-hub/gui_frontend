```python
@ui.page(configs.PAGE_PATH + "2", title=configs.PAGE_TITLE)
async def file_storage2():
    from nicegui import ui
    import time
    import os
    from datetime import datetime

    # 注入自定义 CSS 样式
    ui.add_head_html(f""" <style>{read_css(f"{configs.STATIC_URL}/index.css")}</style> """)

    # 模拟文件存储
    UPLOAD_FOLDER = "uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # 上传进度回调
    def handle_upload(e):
        start_time = time.time()

        # 显示进度条
        progress.visible = True
        for percent in range(100):
            progress_bar.style(f"width: {percent}%")
            time.sleep(0.03)  # 模拟上传延迟

        # 保存文件
        file_path = os.path.join(UPLOAD_FOLDER, e.name)
        with open(file_path, "wb") as f:
            f.write(e.content)

        # 更新文件列表
        refresh_file_list()
        progress.visible = False

        # 显示通知
        ui.notify(f"文件 {e.name} 上传成功！耗时 {time.time() - start_time:.1f}s",
                  type='positive', position='bottom-right')

    # 刷新文件列表
    def refresh_file_list():
        file_grid.clear()
        files = sorted(os.listdir(UPLOAD_FOLDER),
                       key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)),
                       reverse=True)

        with file_grid:
            for filename in files:
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                size = os.path.getsize(filepath) / 1024  # KB

                with ui.card().classes('file-card'):
                    with ui.row().classes('items-center gap-4'):
                        ui.icon('description', size='lg', color='primary')

                        with ui.column():
                            ui.label(filename).classes('text-lg font-medium')
                            with ui.row().classes('text-sm text-gray-600'):
                                ui.label(f"{size:.1f} KB")
                                ui.label("•")
                                ui.label(mtime.strftime("%Y-%m-%d %H:%M"))

                    with ui.row().classes('mt-4 justify-end gap-2'):
                        with ui.button(icon='download', color='green') \
                                .tooltip('下载文件').props('flat dense'):
                            ui.link('', target=filepath).classes('hidden')

                        ui.button(icon='delete', color='red') \
                            .tooltip('删除文件').props('flat dense') \
                            .on('click', lambda f=filename: delete_file(f))

    # 删除文件
    def delete_file(filename):
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        refresh_file_list()
        ui.notify(f"文件 {filename} 已删除", type='warning')

    # 页面布局
    with ui.column().classes('w-full max-w-4xl mx-auto p-8'):
        ui.label("文件存储中心").classes('text-3xl font-bold mb-8')

        # 上传区域
        with ui.column().classes('upload-container'):
            ui.icon('cloud_upload', size='xl', color='primary')
            ui.label("拖放文件到此区域或点击上传").classes('text-lg text-gray-600 mt-2')
            upload = ui.upload(label="选择文件",
                               on_upload=handle_upload,
                               max_file_size=10 * 1024 * 1024)  # 10MB限制
            upload.props('accept=".pdf,.docx,.jpg,.png"')

            with ui.row().classes('mt-4') as progress:
                ui.linear_progress(0).props('instant-feedback').classes('w-64') \
                    .style("--q-linear-progress-track-color: #e9ecef;")
                ui.label('上传中...').classes('text-sm text-gray-600 ml-2')
                progress.visible = False

        # 文件列表区域
        ui.separator().classes('mb-8')
        ui.label("已上传文件").classes('text-xl font-semibold mb-4')
        file_grid = ui.column().classes('w-full gap-4')

    # 初始化文件列表
    refresh_file_list()

```