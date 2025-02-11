import io
import os
import pprint
import subprocess
import uuid
import platform
from types import SimpleNamespace
from typing import BinaryIO

from fastapi import UploadFile
from loguru import logger

from nicegui import ui, app
from nicegui.element import Element
from nicegui.events import UploadEventArguments
from fastapi.responses import StreamingResponse

from nicegui_start_project.utils import get_random_port, sync_to_async
from nicegui_start_project.web_apis import upload_file as upload_file, download_file
from models.mongodb import File

PAGE_TITLE = "文件存储"
PAGE_PATH = "/pages/components/file_storage"


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


def add_element(container: Element, file: File, content: BinaryIO = None) -> None:
    with container:
        with ui.row() as row:
            ui.label(f"{file.filename} - {file.filepath}")

            async def delete_on_click():
                res = await sync_to_async(lambda: File.objects(id=file.id).delete())
                print(type(res), res)
                row.delete()

            async def download_on_click():
                ui.download(f"{PAGE_PATH}/download?uid={file.filepath}")

            ui.button("delete", on_click=delete_on_click)
            ui.button("download", on_click=download_on_click)


@app.get(f"{PAGE_PATH}/download")
async def download(uid: str):
    return await download_file(uid)


@ui.page(PAGE_PATH)
async def file_storage():
    async def on_upload(event: UploadEventArguments):
        filepath = await to_upload_file(event.name, event.content)
        data = dict(filename=event.name, filepath=filepath)
        res: File = await sync_to_async(lambda: File.objects.create(**data))
        print(type(res), res)

        add_element(file_container, res, content=event.content)

        ui.notify(f"Uploaded {event.name}")

    ui.upload(on_upload=on_upload).classes("max-w-full")

    file_container = ui.card()
    for file in await sync_to_async(lambda: File.objects.all()):
        add_element(file_container, file)


if __name__ == "__main__":
    ui.run(host="localhost", port=get_random_port(10086), reload=False, show=False)
