__all__ = ["thread_pool"]

import os
from concurrent import futures


# singleton thread pool
class _ThreadPool:
    # _instance = None

    # note: 这根本就不是单例，因为 __init__ 仍然会执行！
    # def __new__(cls, *args, **kwargs):
    #     if not cls._instance:
    #         cls._instance = super(ThreadPool, cls).__new__(cls)
    #     return cls._instance

    def __init__(self, max_workers=min(32, os.cpu_count() + 4)):
        self._pool = futures.ThreadPoolExecutor(max_workers=max_workers)

    def get_pool(self) -> futures.ThreadPoolExecutor:
        return self._pool

    def submit(self, fn, /, *args, **kwargs):
        return self._pool.submit(fn, *args, **kwargs)

    def shutdown(self, wait=True, *, cancel_futures=False):
        self._pool.shutdown(wait=wait, cancel_futures=cancel_futures)


thread_pool = _ThreadPool()
