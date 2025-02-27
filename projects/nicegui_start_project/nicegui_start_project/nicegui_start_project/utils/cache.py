__all__ = ["simple_cache", "cached"]

import time

from loguru import logger


class _SimpleCache:
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

simple_cache = _SimpleCache()


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


if __name__ == '__main__':
    def test_Cache():  # NOQA
        cache = simple_cache

        # assert cache is SimpleCache()
        expired_time = 3.6
        cache.set(1, 2, expired_time)
        logger.info(cache._cache)
        # logger.info(SimpleCache()._cache)
        logger.info(cache._cache)
        # logger.info(int(expired_time + 0.5))
        # for i in range(int(expired_time + 0.5) + 1):
        #     logger.info(cache.get(1))
        #     time.sleep(1)
        # logger.info(SimpleCache())


    test_Cache()
