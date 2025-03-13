__all__ = ["Reference"]

import ctypes  # ctypes 库直接操作内存地址，模拟 C 语言的指针行为。适用场景：需要与 C 语言库交互。
from typing import Generic, TypeVar

T = TypeVar("T")


class Reference(Generic[T]):
    def __init__(self, value: T):
        self._value = value

    def set(self, value: T):
        self._value = value

    def get(self) -> T:
        return self._value

    def is_null(self):
        return self._value is None

    def __str__(self):
        return str(self._value)


if __name__ == '__main__':
    def test(num: Reference[int]) -> None:
        num.set(2)


    n = Reference[int](123)  # ??? 为什么没有提示？
    print(n)
    test(n)
    print(n)
