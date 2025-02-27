__all__ = [
    "upload_file",
    "download_file",
]

import asyncio
import io
import json
import os
import pprint
import subprocess
import traceback
from typing import Dict, TypedDict, Optional, Any, BinaryIO

import aiohttp
from aiohttp import web, FormData
from aiohttp.client_exceptions import ClientError, ClientResponseError
from loguru import logger
from pydantic import BaseModel

from fastapi import UploadFile
from fastapi.responses import StreamingResponse, Response, JSONResponse

from nicegui_start_project.utils import cached, simple_cache, Maybe, Result


class ErrorResponseDict(TypedDict):
    detail: str


# 能不能直接用 Schema/BaseModel 充当对象，实例化并校验和传递？而不是 TypedDict
class UploadFileResponseDict(TypedDict):
    uid: str


@cached(expire_seconds=0)
def _is_port_listening(port):
    logger.info("call is_port_listening")
    try:
        # Linux 使用 netstat，Windows 使用 netstat
        cmd = ["netstat", "-tuln"] if not os.name == "nt" else ["netstat", "-ano"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return f":{port} " in result.stdout
    except Exception as e:
        logger.error(f"{e}")
        return False


def _check_port_listening(port):
    """ 通过系统命令快速检测（Linux/Windows 兼容） """
    logger.info(simple_cache)

    if not _is_port_listening(port):
        raise RuntimeError(f"Port {port} is not listening.")


async def upload_file(filename: str, content: BinaryIO) -> Result[UploadFileResponseDict, Exception]:
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
        _check_port_listening(12001)
        data = await fetch()
        logger.info(f"upload_file: {type(data)}, {data}")
        return Result.ok(data)
    except Exception as e:
        logger.error(f"{e}\n{traceback.format_exc()}")
        return Result.err(e)


async def download_file(uid: str) -> Result[Response, Dict]:
    # note: 本函数将 download api 封装，这意味着 download api 发生变化的时候，当前函数也可能受影响！
    url = "http://localhost:12001/api/download"

    try:
        # todo: 12001 去配置文件获取
        _check_port_listening(12001)

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=dict(uid=uid)) as response:
                # response.raise_for_status()  # 检查 HTTP 响应状态
                status_code = response.status
                headers = response.headers
                logger.info(pprint.pformat(headers))
                content = await response.content.read()
                if status_code != 200:
                    try:
                        return Result.err(content.decode("utf-8"))
                    except json.JSONDecodeError:
                        return Result.err({"detail": content})
                return Result.ok(Response(status_code=status_code, content=content, headers=headers))
    except Exception as e:
        logger.error(f"{e}\n{traceback.format_exc()}")
        return Result.err({"detail": str(e)})


if __name__ == '__main__':
    # async def main():
    #     with open("./settings.py", "rb") as f:
    #         res = await upload_file("default.py", io.BytesIO(f.read()))
    #     logger.info(res)
    #     res = await download_file(res["uid"])
    #     logger.info(res)
    #
    #
    # asyncio.run(main())

    logger.info(_check_port_listening(12001))
