from nicegui import app

from nicegui_start_project.web_apis import download_file
from . import configs


@app.get(f"{configs.PAGE_PATH}/api/download")
async def download(uid: str):
    return await download_file(uid)
