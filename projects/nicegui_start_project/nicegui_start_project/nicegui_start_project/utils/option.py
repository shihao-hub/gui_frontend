__all__ = ["Maybe", "Option"]

from typing import (
    TypeVar, Generic, Callable,
    Any, Optional as TypingOptional, Union, overload
)
import functools

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E", bound=Exception)


class Maybe(Generic[T]):
    __slots__ = ("_value",)

    def __init__(self, value: Union[T, None]) -> None:
        self._value = value

    @classmethod
    def of(cls, value: T) -> "Maybe[T]":
        """ 非空值构造（若值为空则抛 ValueError） """
        if value is None:
            raise ValueError("Maybe.of() 不接受 None，请使用 Maybe.of_nullable()")
        return cls(value)

    @classmethod
    def of_nullable(cls, value: TypingOptional[T]) -> "Maybe[T]":
        """ 可空值构造 """
        return cls(value)

    @classmethod
    def empty(cls) -> "Maybe[Any]":
        """ 空实例 """
        return cls(None)

    def is_present(self) -> bool:
        """ 值是否存在 """
        return self._value is not None

    def get(self) -> T:
        """ 获取值（若为空则抛 ValueError） """
        if self._value is None:
            raise ValueError("Maybe 为空，无法调用 get()")
        return self._value

    def or_else(self, default: T) -> T:
        """ 存在则返回值，否则返回默认值 """
        return default if self._value is None else self._value

    def or_else_get(self, supplier: Callable[[], T]) -> T:
        """ 存在则返回值，否则通过 supplier 生成默认值 """
        return self._value if self._value is not None else supplier()

    def or_else_throw(self, exception: Union[E, Callable[[], E]]) -> T:
        """存在则返回值，否则抛出异常"""
        if self._value is not None:
            return self._value
        if callable(exception):
            raise exception()
        raise exception

    def if_present(self, consumer: Callable[[T], Any]) -> None:
        """存在则执行 consumer"""
        if self._value is not None:
            consumer(self._value)

    # def filter(self, predicate: Callable[[T], bool]) -> Maybe[T]:
    #     """过滤满足条件的值"""
    #     if self._value is not None and predicate(self._value):
    #         return self
    #     return Maybe.empty()
    #
    # @overload
    # def map(self, mapper: Callable[[T], U]) -> Maybe[U]:
    #     ...
    #
    # @overload
    # def map(self, mapper: Callable[[T], None]) -> Maybe[Any]:
    #     ...
    #
    # def map(self, mapper: Callable[[T], U]) -> Maybe[U]:
    #     """映射值（自动解包 None）"""
    #     if self._value is None:
    #         return Maybe.empty()
    #     mapped = mapper(self._value)
    #     return Maybe.of_nullable(mapped)
    #
    # def flat_map(self, mapper: Callable[[T], Maybe[U]]) -> Maybe[U]:
    #     """链式映射（避免嵌套 Maybe）"""
    #     if self._value is None:
    #         return Maybe.empty()
    #     return mapper(self._value)

    def __eq__(self, other: Any) -> bool:
        """ 比较是否相等 """
        if not isinstance(other, Maybe):
            return False
        return self._value == other._value

    def __repr__(self) -> str:
        """ 调试表示 """
        return f"Maybe({self._value})" if self.is_present() else "Maybe.empty()"

    def __bool__(self) -> bool:
        """ 布尔上下文判断 """
        return self.is_present()


Option = Maybe

if __name__ == '__main__':
    maybe_name = Maybe.of_nullable("Alice")  # Maybe(Alice)
    maybe_empty = Maybe.of_nullable(None)  # Maybe.empty()

    # 异常处理
    # value = Maybe.empty().or_else_throw(ValueError("数据不存在"))  # 抛出 ValueError

    # 消费值
    maybe_name.if_present(print)  # 输出 "Alice"
