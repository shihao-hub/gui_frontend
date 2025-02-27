"""
### 规格
1. 意料之外的异常发生时，会返回包含错误信息的 JSONResponse { detail: str }
   > 注意事项：为什么很多时候，前后端交换返回的都是 200，通过返回的 json 的 code 字段来区分？
   > 就我个人经历发现，ui.download 返回值不是 200 就会有问题... 有点无语

"""

import configparser
import json
import os.path
import sys
import uuid
import yaml
from pathlib import Path
from typing import Dict

from loguru import logger

import uvicorn
from fastapi import FastAPI, Query, File, UploadFile, HTTPException, status
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse

# 运行 main.py，python 似乎会认为 main.py 的所在目录就是 source 目录，所以 nfs.settings 包 python.exe 能找到！
from nfs.settings import NFS_BASE_DIR, configs

FILE_STORAGE_PATH = f"{NFS_BASE_DIR}/files"
PORT = int(configs.get("port"))

# 统一日志目录
# LOG_DIR = Path(f"{BASE_DIR}/logs")
LOG_DIR = Path(f"{NFS_BASE_DIR}/logs")
LOG_DIR.mkdir(exist_ok=True)

# 基础配置
logger.configure(
    handlers=[
        # ----------------------------
        # 控制台输出（开发环境详细）
        # ----------------------------
        {
            "sink": sys.stderr,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{module}:{"
                      "line}</cyan> | <level>{message}</level>",
            "level": "DEBUG",
            "colorize": True,
        },
        # ----------------------------
        # 文件输出（生产环境精简）
        # ----------------------------
        {
            "sink": LOG_DIR / "app_{time:YYYY-MM-DD}.log",
            "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{line} | {message}",
            "level": "INFO",
            "rotation": "00:00",  # 每日轮转
            "retention": "30 days",  # 保留30天
            "compression": "zip",  # 自动压缩旧日志
            "enqueue": True,  # 多进程安全
            "encoding": "utf-8",
        },
        # ----------------------------
        # 错误日志单独存储
        # ----------------------------
        {
            "sink": LOG_DIR / "errors.log",
            "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{line} | {message}\n{exception}",
            "level": "WARNING",
            "retention": "60 days",
            "enqueue": True,
        }
    ],
    # 全局异常捕获（自动记录崩溃信息）
    extra={"common_field": "app_log"},
    activation=[("", True)],  # 启用所有模块日志
)

app = FastAPI()


@app.exception_handler(Exception)
async def universal_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):  # note: 这居然需要自定义？为什么 fastapi 默认不处理？
        # 保留原始 HTTPException 的响应结构
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers
        )
    else:
        # 只要错了都返回 json response ... 但是 StreamingResponse|JSONResponse 这混用岂不是需要 instanceof 参与了？
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)},
        )


@app.post("/api/upload")
async def upload(request: Request, file: UploadFile = File(...)):
    # if file.content_type not in ["text/plain", "application/pdf"]:  # 可根据需求修改
    #     raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Unsupported file type.")
    uid = str(uuid.uuid4())
    filepath = get_filepath(uid)
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)
    with open(get_config_path(uid), "w", encoding="utf-8") as f:
        f.write(json.dumps({"filename": file.filename}, ensure_ascii=False))
    return {"uid": uid}


def get_config_path(uid: str):
    return os.path.join(FILE_STORAGE_PATH, f"{uid}.json")


def get_filepath(uid: str):
    return os.path.join(FILE_STORAGE_PATH, f"{uid}")


def get_config_instance(uid: str) -> Dict:
    with open(get_config_path(uid), "r", encoding="utf-8") as f:
        return json.load(f)


# todo: async
@app.get("/api/download", status_code=status.HTTP_200_OK)
def download(request: Request, uid: str = Query(...)):
    if not os.path.exists(get_config_path(uid)):
        raise HTTPException(status_code=400, detail="文件不存在")
    config = get_config_instance(uid)
    filename = config.get("filename", "unknown")
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(open(get_filepath(uid), "rb"), media_type="application/octet-stream", headers=headers)


if __name__ == '__main__':
    logger.info("nfs service starts successfully.")
    uvicorn.run(app, host="localhost", port=PORT, reload=False)
