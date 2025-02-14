import pprint
import threading
import time

lock = threading.Lock()


def main():
    msg_cache = []
    cnt = 0

    def target():
        nonlocal cnt
        # lock.acquire()
        for i in range(300):
            # msg_cache.append(f"{threading.current_thread().ident} - {i}")
            cnt += 1
            # lock.acquire()
            # print(f"{threading.current_thread().ident} - {i}", flush=True)
            # lock.release()

        # lock.release()

    thread_a = threading.Thread(target=target)
    thread_b = threading.Thread(target=target)
    thread_a.start()
    thread_b.start()

    thread_a.join()
    thread_b.join()

    # print(pprint.pformat(msg_cache))
    print(cnt)


if __name__ == '__main__':
    main()
