"""
### 需求分析
- 基础的文件上传和下载功能

"""

import io
import os
import pprint
import subprocess
import time
import uuid
import platform
from datetime import datetime
from types import SimpleNamespace
from typing import BinaryIO, Dict

from fastapi import UploadFile
from loguru import logger
from PIL import Image

from nicegui import ui, app
from nicegui.element import Element
from nicegui.events import UploadEventArguments
from fastapi.responses import StreamingResponse

from nicegui_start_project import settings
from nicegui_start_project.utils import get_random_port, sync_to_async, read_css, thread_pool
from nicegui_start_project.web_apis import upload_file
from .models import File
from . import configs


async def to_upload_file(filename: str, content: BinaryIO) -> str:
    # content: tempfile.SpooledTemporaryFile
    # print(content, len(content.read()))
    data = await upload_file(filename, content)
    return data.get("uid")


def _is_text_file(filename: str, content: BinaryIO) -> bool:
    if platform.system() in ["Linux", "Darwin"]:
        filepath = ""
        result = subprocess.run(["file", "--mime-type", "-b", filepath], stdout=subprocess.PIPE)
        mime_type = result.stdout.decode().strip()
        return mime_type.startswith("text/")

    # 根据文件名判断
    text_extensions = {".txt", ".csv", ".json", ".xml", ".html", ".md", ".py"}
    _, ext = os.path.splitext(filename)
    if ext.lower() not in text_extensions:
        return False

    # 尝试将二进制数据解码为 UTF-8
    try:
        if content is None:
            return False
        content.read().decode("utf-8")
    except UnicodeDecodeError:
        return False
    except Exception as e:
        logger.error(f"Error while checking if file is text: {e}")
        return False

    return True


def _create_render_dialog(file: File, download_on_click) -> ui.dialog:
    # attention: nfs_service 部署在本地计算机上，可以直接通过路径访问。
    #            但如果是其他服务器，那可能需要封装一下 open，通过 url 无感读取文件（涉及网络 io）
    #            pip3 install fdfs-client-py3==1.0.0（分布式文件系统 fastdfs）
    #            - [fastdfs 基础知识](https://www.cnblogs.com/xiximayou/p/15722444.html)
    filepath = f"{settings.BASE_DIR}/services/nfs_service/files/{file.filepath}"
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()

    with ui.dialog().classes('w-full') as dialog:
        with ui.card().classes('''
            min-w-[95vw] md:min-w-[80vw]  /* 响应式最小宽度 */
            max-w-[95vw] md:max-w-[90vw]  /* 响应式最大宽度 */
            h-[90vh]                     /* 保持高度不变 */
            flex flex-col
        '''):
            # 标题区域
            with ui.row().classes('items-center justify-between px-4 py-2 border-b w-full'):
                # 标题文本左对齐
                ui.label(f"文件预览 - {filename}").classes('text-lg font-semibold')

                # 操作按钮容器右对齐
                with ui.row().classes('items-center gap-2 ml-auto'):
                    ui.button(icon='download', color='green', on_click=download_on_click).props('dense').tooltip('下载')
                    ui.button(icon='close', on_click=dialog.close).props('dense flat').tooltip('关闭')

            # 内容区域容器
            with ui.scroll_area().classes('flex-1 w-full overflow-x-hidden'):  # 自适应高度
                # 根据文件类型显示不同内容
                # todo: 使用重构、设计模式等方法消除显示 if-else
                if ext in ['.png', '.jpg', '.jpeg', '.gif']:  # 图片预览
                    with ui.row().classes('w-full h-full justify-center items-center'):
                        # 未能生效。但是莫名其妙又好了。deepseek 简直是前端的噩梦！
                        # print(filepath)
                        # image = Image.open(filepath)
                        # thread_pool.submit(lambda: image.show())
                        ui.image(filepath).classes('max-h-full object-contain')

                        # deepseek
                        # # 在图片预览部分添加尺寸适配
                        # img = Image.open(filepath)
                        # img.thumbnail((1200, 800))  # 限制最大尺寸
                        # img_bytes = io.BytesIO()
                        # img.save(img_bytes, format='PNG')
                        # ui.image(img_bytes.getvalue()).classes('max-w-full max-h-full object-contain')
                elif ext == '.pdf':  # PDF 预览（需要安装 pyppdf）
                    ui.html(f'''
                        <iframe 
                            src="{filepath}"
                            style="
                                width: 100% !important;
                                height: 100vh !important;  /* 动态高度 */
                                max-height: calc(90vh - 100px); /* 预留标题和按钮空间 */
                                border: none;
                            "
                        ></iframe>
                    ''').classes('w-full h-full')

                elif ext in ['.mp4', '.webm', '.ogg']:  # 视频预览
                    ui.video(filepath).classes('w-full h-auto max-h-full')
                elif ext in ['.csv', '.txt', '.md']:  # 文本文件预览
                    with open(filepath, 'r', encoding="utf-8") as f:
                        content = f.read(5000)  # 限制预览长度
                    ui.code(content).classes('''
                        w-full 
                        max-w-[calc(100%-1rem)]  /* 保留边距空间 */
                        whitespace-pre-wrap
                        break-words
                        bg-gray-50
                        p-4
                        rounded
                    ''')

                else:
                    # 元数据展示优化
                    with ui.column().classes('w-full min-w-0'):
                        ui.label("⚠️ 文件类型不支持直接预览").classes('text-red-500 font-medium')
                        ui.separator()
                        with ui.row().classes('items-center gap-2'):
                            ui.icon('insert_drive_file', size='lg', color='blue')
                            ui.label(filename).classes('font-mono')
                        with ui.grid().classes('grid-cols-2 gap-2'):
                            ui.label("文件大小:").classes('text-gray-600')
                            ui.label(f"{file.filesize / 1024:.1f} KB").classes('font-mono')
                            ui.label("修改时间:").classes('text-gray-600')
                            mtime = datetime.fromtimestamp(file.mtime)
                            ui.label(mtime.strftime("%Y-%m-%d %H:%M")).classes('font-mono')

    return dialog


def _fill_file_card_fns(context: Dict) -> Dict:
    file = context.get("file")
    file_card = context.get("file_card")

    return locals()


def _fill_file_card(file_card, file: File, content: BinaryIO = None):
    with file_card:  # [!code ++]
        with ui.row().classes('items-center gap-4'):
            ui.icon('description', size='lg', color='primary')

            with ui.column():
                # 水平一
                ui.label(file.filename).classes('text-lg font-medium')

                # 水平二
                with ui.row().classes('text-sm text-gray-600'):
                    ui.label(f"{file.filesize / 1024:.1f} KB")
                    ui.label("•")
                    mtime = datetime.fromtimestamp(file.mtime)
                    ui.label(mtime.strftime("%Y-%m-%d %H:%M"))

                # 水平三
                # 操作按钮区域保持右侧对齐
                with ui.row().classes('mt-4 justify-end gap-2'):  # [!code ++]
                    async def _perform_delete():
                        try:
                            # 删除数据库记录
                            res = await sync_to_async(lambda: File.objects(id=file.id).delete())
                            print(type(res), res)

                            # 删除物理文件（根据你的存储服务实现）
                            def delete_file():
                                # todo: nfs_service 应新增删除接口
                                pass

                            await sync_to_async(delete_file)

                            # 移除卡片
                            file_card.delete()

                            ui.notify(f"文件 {file.filename} 已删除", type='positive')
                        except Exception as e:
                            ui.notify(f"删除失败: {str(e)}", type='negative')

                    async def delete_on_click():
                        # 创建确认对话框
                        with ui.dialog() as confirm_dialog:
                            with ui.card().classes('p-4 w-[300px]'):
                                with ui.column().classes('items-center gap-4'):
                                    ui.icon('warning', color='orange', size='lg')
                                    ui.label('确定要删除这个文件吗？').classes('text-lg font-medium')

                                    with ui.row().classes('w-full justify-end gap-2'):
                                        ui.button('取消', on_click=confirm_dialog.close).props('flat')

                                        async def on_click():
                                            confirm_dialog.close()
                                            await _perform_delete()

                                        ui.button('确定', color='red', on_click=on_click).props('unelevated')

                        await confirm_dialog  # 等待用户操作

                    # 创建状态管理变量
                    is_downloading = ui.state(False)

                    async def download_on_click():
                        try:
                            is_downloading.value = True
                            ui.download(f"{configs.PAGE_PATH}/api/download?uid={file.filepath}")
                        finally:
                            # 无论成功与否都恢复按钮
                            is_downloading.value = False

                    async def render_on_click():
                        try:
                            # 创建渲染对话框
                            dialog = _create_render_dialog(file, download_on_click)

                            dialog.open()  # 打开对话框

                        except Exception as e:
                            ui.notify(f"渲染失败: {str(e)}", type='negative')

                    download_button = ui.button(icon='download', color='green', on_click=download_on_click)
                    download_button.tooltip('下载文件').props('flat dense')
                    download_button.bind_visibility_from(is_downloading, 'value', lambda val: not val)

                    delete_button = ui.button(icon='delete', color='red', on_click=delete_on_click)
                    delete_button.tooltip('删除文件').props('flat dense')

                    # 添加渲染按钮
                    render_button = ui.button(icon='preview', color='blue', on_click=render_on_click)
                    render_button.tooltip('预览文件').props('flat dense')


def add_element(file_container: Element, file: File, content: BinaryIO = None) -> None:
    with file_container:
        with ui.card().classes('file-card min-w-[320px]') as file_card:
            _fill_file_card(file_card, file, content)


@ui.page(configs.PAGE_PATH, title=configs.PAGE_TITLE)
async def file_storage():
    async def on_upload(event: UploadEventArguments):
        filepath = await to_upload_file(event.name, event.content)

        def iife_get_filesize():
            binary_file = event.content
            binary_file.seek(0, 2)  # 移动到文件末尾
            filesize = binary_file.tell()  # 获取字节数
            binary_file.seek(0)  # 移动文件指针回到开始
            return filesize

        data = dict(filename=event.name, filepath=filepath, filesize=iife_get_filesize(), mtime=time.time())
        res: File = await sync_to_async(lambda: File.objects.create(**data))
        print(type(res), res)

        add_element(file_container, res, content=event.content)

        ui.notify(f"Uploaded {event.name}")

    # todo: 优化 add css 的方式
    ui.add_head_html(f""" <style>{read_css(f"{configs.STATIC_URL}/index.css")}</style> """)

    with ui.column().classes('w-full max-w-4xl mx-auto p-8'):
        ui.label("文件存储中心").classes('text-3xl font-bold mb-8')
        # 上传区域
        with ui.column().classes('upload-container'):
            ui.icon('cloud_upload', size='xl', color='primary')

            # todo: 实现 拖放文件到此区域或点击上传 功能
            # ui.label("拖放文件到此区域或点击上传").classes('text-lg text-gray-600 mt-2')
            upload = ui.upload(label="选择文件",
                               on_upload=on_upload,
                               max_file_size=10 * 1024 * 1024)  # 10MB限制
            # upload.props('accept=".pdf,.docx,.jpg,.png,.md"')
            upload.classes("max-w-full")

        # 分割线
        ui.separator().classes('mb-8')

        # 文件列表区域
        with ui.column().classes('w-full gap-4'):
            ui.label("已上传文件").classes('text-xl font-semibold mb-4')
            # file_container = ui.row().classes('w-full gap-4 overflow-x-auto')
            file_container = ui.column().classes('w-full gap-4')  # 原垂直布局
            for file in await sync_to_async(lambda: File.objects.all()):
                add_element(file_container, file)
