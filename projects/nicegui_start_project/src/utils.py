__all__ = [
    "ThreadPool",

    "get_random_port",
    "read_html",
    "read_html_head",
    "read_html_body",
]

import functools
import os.path
import re
import socket
from concurrent import futures
from typing import Optional, LiteralString, Literal

from loguru import logger


# singleton thread pool
class ThreadPool:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ThreadPool, cls).__new__(cls)
        return cls._instance

    def __init__(self, max_workers=1):
        self._pool = futures.ThreadPoolExecutor(max_workers=max_workers)

    def submit(self, fn, /, *args, **kwargs):
        return self._pool.submit(fn, *args, **kwargs)

    def shutdown(self, wait=True, *, cancel_futures=False):
        self._pool.shutdown(wait=wait, cancel_futures=cancel_futures)


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


# todo: cache 对接 redis（当然，还需要遵循 如非必要，勿增实体 的原则）
# note: 注释掉的话，html 就可以视为配置文件了，刷新而不需要重启就可以更新 html 内容！
# @functools.cache
def read_html(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def _read_html_tag(filename: str, tag_name: Literal["head", "body"]) -> str:
    content = read_html(filename)
    pattern = re.compile(rf"<{tag_name}>(.*?)</{tag_name}>", re.DOTALL)
    match = pattern.search(content)
    assert match is not None
    return match.group(1)


def read_html_head(filename: str) -> str:
    return _read_html_tag(filename, "head")


def read_html_body(filename: str) -> str:
    return _read_html_tag(filename, "body")


if __name__ == '__main__':
    # ThreadPool
    class A:
        pass


    print(A())
    print(A())
    print(A())
    print(id(A()))
    print(A() is A())
    print(ThreadPool() is ThreadPool())
    print(id(ThreadPool()), id(ThreadPool()))
    assert id(ThreadPool()) == id(ThreadPool())  # 为什么始终成立？id 我记得是比较地址的呀... 《流畅的 Python》
    assert ThreadPool() is ThreadPool()
    # get_random_port
    pass
    print(get_random_port(8080))
