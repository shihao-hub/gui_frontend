import io
from typing import Union

from nicegui import app
from fastapi import HTTPException, status, Response
from fastapi.responses import StreamingResponse

from loguru import logger

from nicegui_start_project.web_apis import download_file
from . import configs


@app.get(f"{configs.PAGE_PATH}/api/download")
async def download(uid: str):
    res_response = await download_file(uid)
    if res_response.is_err():
        logger.error(f"download file error: {res_response.unwrap_err()}")
        # raise HTTPException(status_code=400, detail=f"{res_response.unwrap_err()}")
        # ui.download 必须返回文件流，raise HTTPException 返回的响应浏览器会有下载表现，但是提示：无法下载 - 出现问题
        # 因此我选择返回一个 error 文件，提示用户下载失败
        filename = "error.json"
        headers = {"Content-Disposition": f"attachment; filename={filename}"}

        content = f"{res_response.unwrap_err()}".encode("utf-8")
        bytesio = io.BytesIO()
        bytesio.write(content)
        bytesio.seek(0)

        return StreamingResponse(bytesio, status_code=200, media_type="application/octet-stream", headers=headers)
    return res_response.unwrap()
