__all__ = [
    "thread_pool",

    "cached",
    "simple_cache",

    "get_random_port",
    "sync_to_async",

    "read_html",
    "read_css",
    "read_js",
    "read_html_head",
    "read_html_body",

    "get_package_path"
]

import asyncio
import functools
import os.path
import re
import socket
import time
from concurrent import futures
from pathlib import Path
from typing import Optional, LiteralString, Literal

from loguru import logger


# singleton thread pool
class ThreadPool:
    # _instance = None

    # note: 这根本就不是单例，因为 __init__ 仍然会执行！
    # def __new__(cls, *args, **kwargs):
    #     if not cls._instance:
    #         cls._instance = super(ThreadPool, cls).__new__(cls)
    #     return cls._instance

    def __init__(self, max_workers=3):
        self._pool = futures.ThreadPoolExecutor(max_workers=max_workers)

    def get_pool(self) -> futures.ThreadPoolExecutor:
        return self._pool

    def submit(self, fn, /, *args, **kwargs):
        return self._pool.submit(fn, *args, **kwargs)

    def shutdown(self, wait=True, *, cancel_futures=False):
        self._pool.shutdown(wait=wait, cancel_futures=cancel_futures)


class SimpleCache:
    """
    ### **5. 性能优化方向**
    - **定期清理**：后台线程定时执行 `clear_expired()`（需线程安全）。
    - **内存优化**：使用 `__slots__` 减少对象内存开销。
    - **序列化**：支持存储复杂对象（如通过 `pickle`）。
    """

    # _instance = None
    #
    # def __new__(cls, *args, **kwargs):
    #     if not cls._instance:
    #         cls._instance = super(SimpleCache, cls).__new__(cls)
    #     return cls._instance

    # 以下内容是 deepseek r1 的回答，很好用！
    def __init__(self):
        self._cache = {}

    def set(self, key, value, expire_seconds=0.0):
        """ 设置缓存（expire_seconds=0 表示永不过期） """
        expire_ts = time.time() + expire_seconds if expire_seconds > 0 else 0
        self._cache[key] = (value, expire_ts)  # note: 数组 or 具名数组

    def _is_expired(self, key):
        if key not in self._cache:
            return False

        value = self._cache[key]
        return 0 < value[1] < time.time()

    def get(self, key, default=None):
        """ 获取缓存值，自动清理过期键 """
        if key not in self._cache:
            return default

        if self._is_expired(key):  # note: get 的时候尝试清理
            del self._cache[key]
            return default
        return self._cache[key][0]

    # def clear_expired(self, key):
    #     if self._is_expired(key):
    #         del self._cache[key]

    def clear_all_expired(self):
        """ 手动清理所有过期键 """
        expired_keys = [k for k in self._cache.keys() if self._is_expired(k)]
        for k in expired_keys:  # note: 在遍历 dict.keys() 的时候不允许删除
            del self._cache[k]

    def size(self):
        """ 返回当前有效缓存数量 """
        self.clear_all_expired()  # note: size 的时候清理
        return len(self._cache)

    def __str__(self):
        return f"size: {self.size()}, cache: {dict([(k, v[0]) for k, v in self._cache.items()])}"

    def __repr__(self):
        return f"{self.__class__.__name__}()"


# class LRUCache(SimpleCache):
#     """ 容量限制 """
#
#     def __init__(self, max_size=100):
#         super().__init__()
#         self.max_size = max_size
#         self._order = []
#
#     def set(self, key, value, expire_seconds=0):  # 当前实现为简化版，实际 LRU 需在 **访问时更新顺序**
#         super().set(key, value, expire_seconds)  # note: super()
#         self._order.append(key)  # LRU: 删除最老的
#         if len(self._order) > self.max_size:
#             old_key = self._order.pop(0)
#             if old_key in self._cache:
#                 del self._cache[old_key]

simple_cache = SimpleCache()
thread_pool = ThreadPool()


def cached(expire_seconds=0):
    """
    Usage:
        @cached(expire_seconds=10)
        def heavy_calculation(x):
            print("Computing...")
            return x * x
    """

    def decorator(func):
        cache = simple_cache

        def wrapper(*args, **kwargs):
            key = f"{func.__name__}-{args}-{kwargs}"
            value = cache.get(key)
            if value is None:
                value = func(*args, **kwargs)
                cache.set(key, value, expire_seconds)
            return value

        return wrapper

    return decorator


async def sync_to_async(func, *args, **kwargs):
    def sync_code():
        return func(*args, **kwargs)

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(thread_pool.get_pool(), sync_code)


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


def read_css(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def read_js(filename: str) -> str:
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


def get_package_path(file: str):
    relative_path = str(Path(file).resolve().relative_to(Path.cwd()))
    extension = Path(file).suffix
    relative_path = relative_path.replace("\\", ".")
    relative_path = relative_path.replace("/", ".")
    return relative_path[: -len(extension)]


if __name__ == '__main__':
    # ThreadPool
    def test_ThreadPool():  # NOQA
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


    def test_Cache():  # NOQA
        cache = simple_cache

        # assert cache is SimpleCache()
        expired_time = 3.6
        cache.set(1, 2, expired_time)
        print(cache._cache)
        # print(SimpleCache()._cache)
        print(cache._cache)
        # print(int(expired_time + 0.5))
        # for i in range(int(expired_time + 0.5) + 1):
        #     print(cache.get(1))
        #     time.sleep(1)
        # print(SimpleCache())


    # test_Cache()

    def test_get_package_path():
        res = get_package_path(__file__)
        print(type(res), res)
        print(type(__file__), __file__)


    test_get_package_path()
