__all__ = [
    "sync_to_async",

    "cached", "simple_cache",

    "read_html", "read_css", "read_js", "read_sql", "read_html_head", "read_html_body",

    "thread_pool",

    "Maybe", "Option",

    "Result",

    "mvc",

    "SingletonMeta", "APIService",
    "catch_unhandled_exception", "get_random_port", "get_package_path",
    "get_mongonengine_meta",
]

import functools
import inspect
import socket
import traceback
from typing import Generic, TypeVar, List, Type
from pathlib import Path
from typing import Optional

from loguru import logger  # NOQA

from nicegui_start_project.settings import database_manager, DATABASE_ALIAS
from . import async_utils, cache, file_utils, mvc, option, result, thread_utils
from .mediator import SingletonMeta

T = TypeVar("T")

sync_to_async = async_utils.sync_to_async  # NOQA

cached = cache.cached
simple_cache = cache.simple_cache

read_html_head = file_utils.read_html_head
read_html_body = file_utils.read_html_body
read_html = file_utils.read_html
read_css = file_utils.read_css
read_js = file_utils.read_js
read_sql = file_utils.read_sql

Maybe = option.Maybe
Option = option.Option

Result = result.Result

thread_pool = thread_utils.thread_pool


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


class _PackagePath:
    def __init__(self, package_path: str):
        self.package_path = package_path
        assert self.package_path.count(".") >= 2
        self.package_path_parent = self.package_path[:self.package_path.rfind(".")]

    def __str__(self):
        return self.package_path


def get_package_path(file: str):
    """
    Usage:
        {source}/pages/components/sample/pages.py
        get_package_path(__file__) -> pages.components.sample.pages
    """
    relative_path = str(Path(file).resolve().relative_to(Path.cwd()))
    extension = Path(file).suffix
    relative_path = relative_path.replace("\\", ".")
    relative_path = relative_path.replace("/", ".")
    res = relative_path[: -len(extension)]
    assert res.startswith("pages.components")
    return _PackagePath(res)


def catch_unhandled_exception(func):
    """捕获出乎意料的异常的装饰器，该装饰器既可以修饰普通函数，又可以修饰 async 函数"""
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


def persistent_func_cache_data(table_name: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            return res

        return wrapper

    return decorator


def get_mongonengine_meta(collection: str):
    return dict(collection=collection, db_alias=DATABASE_ALIAS)


class APIService(Generic[T]):
    """参考 django APIView"""

    def __init__(self, document_class: Type[T]):
        self._document_class = document_class

    def create(self, **kwargs) -> T:
        this = self
        doc = self._document_class(**kwargs)
        doc.save()
        return doc

    def delete(self, doc: T) -> bool:
        this = self
        return doc.delete()

    def update(self, doc: T, **kwargs) -> T:
        this = self
        for k, v in kwargs.items():
            setattr(doc, k, v)
        doc.save()
        return doc

    def get(self, doc_id: str) -> T:
        this = self
        return self._document_class.objects.get(id=doc_id)

    def lists(self) -> List[T]:
        this = self
        return self._document_class.objects.all()


if __name__ == '__main__':
    def test_get_package_path():
        res = get_package_path(__file__)
        logger.info("{}\t{}", type(res), res)
        logger.info("{}\t{}", type(__file__), __file__)


    test_get_package_path()
