import json
import os.path
import uuid
from pathlib import Path
from typing import Dict

import uvicorn
from fastapi import FastAPI, Query, File, UploadFile, HTTPException, status
from fastapi.requests import Request
from starlette.responses import StreamingResponse

from nicegui_start_project.utils import get_random_port

# todo: 如何做到支持 . .. 导入呢？

NFS_BASE_DIR = Path(__file__).parent.parent
NFS_SOURCE_DIR = Path(__file__).parent

FILE_STORAGE_PATH = f"{NFS_BASE_DIR}/ignore_files"

app = FastAPI()


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
    uvicorn.run(app, host="localhost", port=12001, reload=False)
