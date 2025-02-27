__all__ = ["Result", "resultify"]

from typing import (
    TypeVar, Generic, Callable, Union,
    Any, Optional, overload
)
import functools

T = TypeVar("T")  # ok
U = TypeVar("U")
E = TypeVar("E")  # error
F = TypeVar("F")


class Result(Generic[T, E]):
    """ 模拟 Rust 的 Result 类型 """

    def __init__(self, value: Union[T, E], is_ok: bool) -> None:
        self._value = value
        self._is_ok = is_ok

    @classmethod
    def ok(cls, value: T) -> "Result[T, Any]":
        """成功结果"""
        return cls(value, is_ok=True)

    @classmethod
    def err(cls, error: E) -> "Result[Any, E]":
        """ 失败结果 """
        return cls(error, is_ok=False)

    def is_ok(self) -> bool:
        """ 是否成功 """
        return self._is_ok

    def is_err(self) -> bool:
        """ 是否失败 """
        return not self._is_ok

    # def map(self, op: Callable[[T], U]) -> Result[U, E]:
    #     """ 映射成功值，保持错误不变 """
    #     return self.and_then(lambda v: Result.ok(op(v)))
    #
    # def map_err(self, op: Callable[[E], F]) -> Result[T, F]:
    #     """ 映射错误值，保持成功不变 """
    #     if self.is_ok():
    #         return self
    #     return Result.err(op(self._value))
    #
    # def and_then(self, op: Callable[[T], Result[U, E]]) -> Result[U, E]:
    #     """ 链式操作（成功时继续，失败则短路） """
    #     if self.is_ok():
    #         return op(self._value)
    #     return Result.err(self._value)
    #
    # def or_else(self, op: Callable[[E], Result[T, F]]) -> Result[T, F]:
    #     """ 处理错误（失败时继续，成功则短路） """
    #     if self.is_ok():
    #         return self
    #     return op(self._value)

    def unwrap(self) -> T:
        """ 解包成功值（失败时抛异常） """
        if self.is_ok():
            return self._value
        raise ValueError(f"试图解包错误值: {self._value}")

    def unwrap_err(self) -> E:
        """解包错误值（成功时抛异常）"""
        if self.is_err():
            return self._value
        raise ValueError(f"试图解包成功值: {self._value}")

    # def expect(self, msg: str) -> T:
    #     """ 解包成功值，失败时抛自定义异常 """
    #     if self.is_ok():
    #         return self._value
    #     raise ValueError(f"{msg}: {self._value}")

    def __eq__(self, other: Any) -> bool:
        """ 比较是否相等 """
        if not isinstance(other, Result):
            return False
        return (self._is_ok == other._is_ok) and (self._value == other._value)

    def __repr__(self) -> str:
        """调试表示"""
        return f"Ok({self._value})" if self.is_ok() else f"Err({self._value})"


# 装饰器：自动将异常转换为 Result.err
def resultify(func: Callable[..., T]) -> Callable[..., Result[T, Exception]]:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Result[T, Exception]:
        try:
            return Result.ok(func(*args, **kwargs))
        except Exception as e:
            return Result.err(e)

    return wrapper
