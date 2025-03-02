__all__ = [
    "sync_to_async",

    "cached",
    "simple_cache",

    "read_html",
    "read_css",
    "read_js",
    "read_html_head",
    "read_html_body",

    "thread_pool",

    "Maybe",
    "Result",

    "catch_unhandled_exception",
    "get_random_port",
    "get_package_path",
]

import functools
import inspect
import socket
import traceback
from pathlib import Path
from typing import Optional, Callable

from loguru import logger

from .async_utils import sync_to_async
from .cache import cached, simple_cache
from .file_utils import read_html, read_css, read_js, read_html_head, read_html_body
from .thread_pool import thread_pool
from .option import Maybe, Option
from .result import Result


def _is_port_in_use(port: int) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(("localhost", port))
    except Exception as e:
        logger.error(f"Error checking port {port}: {e}")
        return False
    finally:
        sock.close()
    return True


def get_random_port(port: Optional[int] = None) -> int:
    """
    :param port: the port number to check, if it is not available, a random port will be selected.
    :return: an available port number
    """
    if port and _is_port_in_use(port):
        return port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 绑定到地址（"localhost"）和端口0，0表示让系统选择可用的端口
        s.bind(("localhost", 0))
        # 获取绑定的端口号
        return s.getsockname()[1]


def get_package_path(file: str):
    relative_path = str(Path(file).resolve().relative_to(Path.cwd()))
    extension = Path(file).suffix
    relative_path = relative_path.replace("\\", ".")
    relative_path = relative_path.replace("/", ".")
    return relative_path[: -len(extension)]


def catch_unhandled_exception(func):
    if inspect.iscoroutine(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.error(f"{e}\n{traceback.format_exc()}")
    else:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"{e}\n{traceback.format_exc()}")
    return wrapper


if __name__ == '__main__':
    def test_get_package_path():
        res = get_package_path(__file__)
        logger.info("{}\t{}", type(res), res)
        logger.info("{}\t{}", type(__file__), __file__)


    test_get_package_path()
