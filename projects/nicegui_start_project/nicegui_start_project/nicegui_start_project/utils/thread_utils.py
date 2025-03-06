__all__ = ["thread_pool"]

import os
from concurrent import futures

from loguru import logger


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

if __name__ == '__main__':
    def test_ThreadPool():  # NOQA
        class A:
            pass

        logger.info(A())
        logger.info(A())
        logger.info(A())
        logger.info(id(A()))
        logger.info(A() is A())
        logger.info(_ThreadPool() is _ThreadPool())
        logger.info(f"{id(_ThreadPool())}\t{id(_ThreadPool())}")
        assert id(_ThreadPool()) == id(_ThreadPool())  # 为什么始终成立？id 我记得是比较地址的呀... 《流畅的 Python》
        assert _ThreadPool() is _ThreadPool()
        # get_random_port
