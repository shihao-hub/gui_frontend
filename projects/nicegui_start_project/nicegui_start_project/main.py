import atexit
import importlib
import os
import pprint
import subprocess
import sys
from typing import List, Callable, Dict

import mongoengine as engine
from fastapi.routing import APIRoute
from loguru import logger

from nicegui import ui, app

from nicegui_start_project.settings import (
    HOST, PORT, BASE_URL, SOURCE_DIR, BASE_DIR,
    DATABASE, DATABASE_ALIAS
)


def init_database():
    engine.connect(db=DATABASE, alias=DATABASE_ALIAS, host="localhost", port=27017)


def start_services() -> Callable:
    python_exe = sys.executable  # deepseek 666

    # 启动另一个程序（非阻塞）
    nfs_service = subprocess.Popen(
        [sys.executable, f"{BASE_DIR}/services/nfs_service/nfs/main.py"],  # 参数列表
        shell=True,  # Windows 需要此参数识别 .exe
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    atexit.register(nfs_service.terminate)  # 确保父进程退出前终止子进程

    def wait():
        nfs_service.wait()

    return wait


def main():
    start_services()

    init_database()

    def url_join(snippets: List[str]) -> str:
        return "/".join([e.strip("/") for e in snippets])

    with ui.column():
        root_dir = f"{SOURCE_DIR}/pages/components"
        for dirname in os.listdir(f"{SOURCE_DIR}/pages/components"):
            if not os.path.isdir(f"{root_dir}/{dirname}") or dirname.startswith("_"):
                continue
            # 体现了约定大于配置？
            try:
                # import code
                importlib.import_module(f"pages.components.{dirname}.pages")
                try:
                    importlib.import_module(f"pages.components.{dirname}.routers")
                except ImportError:
                    pass

                module = importlib.import_module(f"pages.components.{dirname}.configs")
                page_title = getattr(module, "PAGE_TITLE", None)
                page_path = getattr(module, "PAGE_PATH", None)
                if page_title and page_path:
                    link = ui.link(page_title, url_join([BASE_URL, page_path]))
                    link.props(""" target="_blank" """)
            except Exception as e:
                logger.error(f"Error importing module {dirname}: {e}")
    print(pprint.pformat([f"{e.path} - {e.methods}" for e in app.routes if isinstance(e, APIRoute)]))
    ui.run(host=HOST, port=PORT, reload=False, show=False, favicon="🚀")


if __name__ == '__main__':
    main()
