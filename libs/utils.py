__all__ = ["Module"]

from abc import ABC, abstractmethod


class Module(ABC):
    @abstractmethod
    def run(self):
        # 注意，其他类继承 ABC 并实现的时候，如果是抽象函数，self 未使用也不会有波浪线提示。难道 PyCharm 是为了让我们习惯性定义接口？
        pass
