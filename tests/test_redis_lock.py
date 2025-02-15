import threading

import redis
import time


class RedisLock:
    def __init__(self, redis_host, redis_port, lock_key):
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port)
        self.lock_key = lock_key
        self.lock_value = "1"

    def acquire_lock(self, expire_time=10):
        """ 获取锁 """
        while True:
            # 尝试设置锁
            if self.redis_client.setnx(self.lock_key, self.lock_value):
                # 设置过期时间
                self.redis_client.expire(self.lock_key, expire_time)
                return True
            # 如果锁已经被其他进程获取，则等待一段时间后重试
            time.sleep(0.01)

    def release_lock(self):
        """释放锁"""
        self.redis_client.delete(self.lock_key)


if __name__ == '__main__':
    redis_lock = RedisLock("localhost", 6379, "my_lock")

    msg_cache = []
    cnt = 0
    lock = threading.Lock()


    def target():
        global cnt
        time.sleep(1)

        def fn():
            for i in range(100):
                # msg_cache.append(f"{threading.current_thread().ident} - {i}")
                # cnt += 1
                # lock.acquire()
                print(f"{threading.current_thread().ident} - {i}", flush=True)
                # lock.release()

        if redis_lock.acquire_lock():
            try:
                fn()
                # time.sleep(5)
            finally:
                redis_lock.release_lock()

        # lock.acquire()
        # fn()
        # lock.release()


    thread_a = threading.Thread(target=target)
    thread_b = threading.Thread(target=target)
    thread_a.start()
    thread_b.start()

    thread_a.join()
    thread_b.join()

    print(cnt)
