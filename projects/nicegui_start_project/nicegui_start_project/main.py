import atexit
import importlib
import subprocess
import sys
from typing import List, Callable

from nicegui import ui

from pages import components
from nicegui_start_project.settings import HOST, PORT, BASE_URL, SOURCE_DIR, BASE_DIR
from apps.api.routers import register_routers

# importlib.import_module("projects.nicegui_start_project.src.pages.components.todolists.todolists")

register_routers()


def url_join(snippets: List[str]) -> str:
    return "/".join([e.strip("/") for e in snippets])


def main():
    with ui.column():
        modules = []
        for name in dir(components):
            if name.startswith("_"):
                continue
            module = getattr(components, name)
            if hasattr(module, "PAGE_TITLE") and hasattr(module, "PAGE_PATH"):
                modules.append(module)
        modules.sort(key=lambda x: getattr(x, "PAGE_TITLE"))
        for module in modules:
            link = ui.link(getattr(module, "PAGE_TITLE"), url_join([BASE_URL, getattr(module, "PAGE_PATH")]))
            link.props(""" target="_blank" """)


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


if __name__ == '__main__':
    start_services()
    main()
    ui.run(host=HOST, port=PORT, reload=False, show=False, favicon="🚀")
