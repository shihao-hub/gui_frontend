__all__ = [
    "MongoAPIService",
    "catch_unhandled_exception", "get_random_port", "get_package_path",
    "get_mongonengine_meta",
]

import functools
import inspect
import socket
import traceback
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Type, Iterable, Any
from pathlib import Path
from typing import Optional

from loguru import logger

from nicegui_start_project.settings import database_manager, DATABASE_ALIAS

T = TypeVar("T")


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


class PackagePath:
    def __init__(self, package_path: str):
        self.package_path = package_path
        assert self.package_path.count(".") >= 2
        self.package_path_parent = self.package_path[:self.package_path.rfind(".")]

    def __str__(self):
        return self.package_path


def get_package_path(file: str) -> PackagePath:
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
    return PackagePath(res)


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


class MongoAPIService(Generic[T]):
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


class Module(ABC):
    @abstractmethod
    def call(self): ...


class ListLikeSet:
    def __init__(self, iterable: Optional[Iterable] = None):
        self._data = set()
        self._order = []  # 用列表维护插入顺序以实现有序性

        self._init_data(iterable)

    def _init_data(self, iterable: Optional[Iterable] = None):
        if iterable is None:
            return
        for item in iterable:
            self.append(item)  # 个人不推荐在 private 中调用 public 方法，如果 public 调用 public 方法，则需要 mediator 介入

    def _element_exist(self, item):
        return item in self._data

    def append(self, item):
        """添加元素到末尾（如果不存在）"""
        if self._element_exist(item):
            return
        self._data.add(item)
        self._order.append(item)

    def insert(self, index, item):
        """插入元素到指定位置（如果不存在）"""
        if self._element_exist(item):
            return
        self._data.add(item)
        self._order.insert(index, item)

    def extend(self, iterable: Iterable):
        """扩展元素（跳过已存在的元素）"""
        for item in iterable:
            self.append(item)

    def remove(self, item):
        """移除元素"""
        if self._element_exist(item):
            return
        self._data.remove(item)
        self._order.remove(item)

    def pop(self, index=-1) -> Any:
        """弹出指定位置的元素"""
        item = self._order.pop(index)
        self._data.remove(item)
        return item

    def index(self, item, start=0, end: Optional[int] = None) -> int:
        """返回元素的索引"""
        if end is None:
            end = len(self._order)
        try:
            return self._order.index(item, start, end)
        except ValueError:
            raise ValueError(f"{item} is not in list")

    def count(self, item):
        """统计元素出现次数（只能是 0 或 1）"""
        return 1 if item in self._data else 0

    def sort(self, key=None, reverse=False):
        """排序（直接修改内部顺序列表）"""
        self._order.sort(key=key, reverse=reverse)

    def reverse(self):
        """反转顺序"""
        self._order = self._order[::-1]

    def __getitem__(self, index):
        """支持索引和切片访问"""
        if isinstance(index, slice):
            return self.__class__(self._order[index])
        return self._order[index]

    def __setitem__(self, index, value):
        """修改指定位置的元素（需确保唯一性）"""
        old_item = self._order[index]

        if value == old_item:
            return
        if self._element_exist(value):
            raise ValueError(f"Value {value} already exists")

        self._data.remove(old_item)
        self._data.add(value)
        self._order[index] = value

    def __delitem__(self, index):
        """删除指定位置的元素"""
        item = self._order[index]
        del self._order[index]
        self._data.remove(item)

    def __len__(self):
        return len(self._order)

    def __contains__(self, item):
        return item in self._data

    def __iter__(self):
        return iter(self._order)

    def __repr__(self):
        return f"ListLikeSet({self._order})"


if __name__ == '__main__':
    def test_get_package_path():
        res = get_package_path(__file__)
        logger.info("{}\t{}", type(res), res)
        logger.info("{}\t{}", type(__file__), __file__)


    test_get_package_path()
