__all__ = [
    "get_users",

    "upload_file",
    "download_file",
]

import asyncio
import io
import os
import pprint
import subprocess
import traceback
from typing import Dict, TypedDict, Optional, Any, BinaryIO

from fastapi import UploadFile
from pydantic import BaseModel

import aiohttp
from aiohttp import web, FormData
from loguru import logger

from fastapi.responses import StreamingResponse, Response


# 这个能不能这样？直接用 Schema/BaseModel 充当对象，实例化并校验和传递
class GetUsersBodySchema(BaseModel):
    pass


class GetUsersBody(TypedDict):
    pass


def get_users(body: GetUsersBody):
    pass


class UploadFileResponse(TypedDict):
    uid: str


def _check_port_listening(port):
    """ 通过系统命令快速检测（Linux/Windows 兼容） """

    def is_port_listening():
        try:
            # Linux 使用 netstat，Windows 使用 netstat
            cmd = ["netstat", "-tuln"] if not os.name == "nt" else ["netstat", "-ano"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return f":{port} " in result.stdout
        except Exception as e:
            print(f"Error: {e}")
            return False

    if not is_port_listening():
        raise RuntimeError(f"Port {port} is not listening.")


async def upload_file(filename: str, content: BinaryIO) -> UploadFileResponse:
    url = "http://localhost:12001/api/upload"

    async def fetch() -> Dict:
        async with aiohttp.ClientSession() as session:
            form_data = FormData()
            form_data.add_field(
                name="file",
                value=io.BytesIO(content.read()),
                filename=filename,
                content_type="application/octet-stream"
            )
            async with session.post(url, data=form_data) as response:
                response.raise_for_status()  # 检查 HTTP 响应状态
                return await response.json()  # response 类比 js 的 Promise

    try:
        data = await fetch()
        print(f"upload_file: {type(data)}, {data}")
        return data
    except Exception as e:
        logger.error(f"{e}\n{traceback.format_exc()}")


async def download_file(uid: str):
    url = "http://localhost:12001/api/download"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=dict(uid=uid)) as response:
                response.raise_for_status()  # 检查 HTTP 响应状态
                status_code = response.status
                headers = response.headers
                print(pprint.pformat(headers), flush=True)
                content = await response.content.read()
                return Response(status_code=status_code, content=content, headers=headers)
    except Exception as e:
        logger.error(f"{e}\n{traceback.format_exc()}")


if __name__ == '__main__':
    # async def main():
    #     with open("./settings.py", "rb") as f:
    #         res = await upload_file("default.py", io.BytesIO(f.read()))
    #     print(res)
    #     res = await download_file(res["uid"])
    #     print(res)
    #
    #
    # asyncio.run(main())

    print(_check_port_listening(12001))
