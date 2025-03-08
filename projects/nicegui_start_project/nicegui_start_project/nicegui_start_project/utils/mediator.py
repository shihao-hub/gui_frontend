__all__ = ["thread_pool", "SingletonMeta"]

import threading


def thread_pool():
    from .thread_utils import thread_pool as thread_pool_alias
    return thread_pool_alias


class SingletonMeta(type):
    _instances = {}  # fixme: 这个得弱引用吧？即若某个对象只被 _instances 持有，垃圾回收器会回收它
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
