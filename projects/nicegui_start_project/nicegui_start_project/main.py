import atexit
import importlib
import logging
import os
import pprint
import subprocess
import sys
import traceback
from typing import List, Callable, Dict

import mongoengine as engine
from fastapi.routing import APIRoute
from loguru import logger

from nicegui import ui, app

from nicegui_start_project.settings import (
    HOST, PORT, BASE_URL,
    DATABASE, DATABASE_ALIAS,
    NFS_SERVICE_STARTUP_ENTRY_PATH,
    COMPONENTS_ROOT_DIR,
    COMPONENTS_PACKAGE_NAME,
)


def init_database():
    engine.connect(db=DATABASE, alias=DATABASE_ALIAS, host="localhost", port=27017)


def init_logger():
    # 禁用标准logging模块
    logging.disable(logging.CRITICAL)

    # 移除默认配置（避免与自定义配置冲突）
    logger.remove()

    # 基础配置常量
    log_level = os.getenv("LOG_LEVEL", "DEBUG")  # 环境变量优先
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    # 核心配置函数
    def configure_logger():
        # 控制台输出配置
        logger.add(
            sys.stderr,
            level=log_level,
            format=log_format,
            backtrace=True,  # 显示完整异常堆栈
            diagnose=True,  # 显示变量值调试信息（生产环境应关闭）
            enqueue=True,  # 线程安全模式
        )

        # 文件输出配置（按需求选择）
        logger.add(
            "../logs/app_{time:YYYY-MM-DD}.log",
            rotation="00:00",  # 每天零点切割
            retention="30 days",  # 保留30天
            compression="zip",  # 压缩旧日志
            level="INFO",  # 文件日志级别
            enqueue=True,
            format=log_format,
        )

    configure_logger()

    # 可选：捕获所有未处理异常
    def handle_exception(exc_type, exc_value, exc_traceback):
        logger.exception(f"Uncaught exception occurred: ")
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    # sys.excepthook = handle_exception


def start_services() -> Callable:
    python_exe = sys.executable  # deepseek 666

    # fixme: 启动失败为什么没有提示？

    # 启动另一个程序（非阻塞）
    nfs_service = subprocess.Popen(
        [sys.executable, NFS_SERVICE_STARTUP_ENTRY_PATH],  # 参数列表
        shell=True,  # Windows 需要此参数识别 .exe
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    atexit.register(nfs_service.terminate)  # 确保父进程退出前终止子进程

    def wait():
        nfs_service.wait()

    return wait


def _add_css():
    css = """
    /* 主容器 */
    .card-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    /* 卡片样式 */
    .service-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 2px solid transparent;
        cursor: pointer;
        text-decoration: none !important;
    }

    .service-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
        border-color: #3B82F6;
    }

    /* 卡片内容 */
    .card-content {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .card-icon {
        font-size: 1.5rem;
    }

    .card-title {
        font-size: 1.1rem;
        font-weight: 500;
        color: #1F2937;
        margin: 0;
    }

    /* 响应式优化 */
    @media (max-width: 640px) {
        .card-container {
            grid-template-columns: 1fr;
            padding: 1rem;
        }
    }
    """
    ui.add_head_html(f""" <style>{css}</style> """)


def main():
    start_services()

    init_database()
    init_logger()

    def url_join(snippets: List[str]) -> str:
        return "/".join([v.strip("/") for v in snippets])

    _add_css()

    with ui.column().classes('card-container'):
        for dirname in os.listdir(COMPONENTS_ROOT_DIR):
            if dirname.startswith("_") or not os.path.isdir(f"{COMPONENTS_ROOT_DIR}/{dirname}"):
                continue
            # 体现了约定大于配置？
            try:
                # import code
                importlib.import_module(f"{COMPONENTS_PACKAGE_NAME}.{dirname}.pages")
                try:
                    importlib.import_module(f"{COMPONENTS_PACKAGE_NAME}.{dirname}.routers")
                except ImportError:
                    pass

                module = importlib.import_module(f"{COMPONENTS_PACKAGE_NAME}.{dirname}.configs")
                page_title = getattr(module, "PAGE_TITLE", None)
                page_path = getattr(module, "PAGE_PATH", None)
                page_icon = getattr(module, "PAGE_ICON", None)
                version = getattr(module, "VERSION", "").strip()
                if page_title and page_path:
                    card_classes = "service-card"
                    if not version.startswith("1"):  # 卡片背景置灰
                        card_classes += " bg-gray-200"
                    link = ui.link(page_title, url_join([BASE_URL, page_path]))
                    link.classes(card_classes)
                    link.props(""" target="_blank" """)
                    with link, ui.row().classes('card-content'):
                        ui.label(page_icon or "📄").classes('card-icon')
                        ui.label(page_title).classes('card-title')

                    if version:  # 可选：添加版本角标（浮动角标）
                        with link:
                            ui.badge(version).classes('absolute top-2 right-2 text-xs')
                else:
                    logger.warning(f"Module '{dirname}' does not have 'PAGE_TITLE' or 'PAGE_PATH' defined.")
            except Exception as e:
                logger.error(f"Error importing module {dirname}: {e}\n{traceback.format_exc()}")
    logger.info(pprint.pformat([f"{e.path} - {e.methods}" for e in app.routes if isinstance(e, APIRoute)]))
    ui.run(host=HOST, port=PORT, reload=False, show=False, favicon="🚀")


if __name__ == '__main__':
    main()
