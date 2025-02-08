from multiprocessing import Process
import time


def worker():
    while True:
        print("子进程正在工作...", flush=True)
        time.sleep(1)


if __name__ == '__main__':
    # 创建并启动子进程
    p = Process(target=worker)
    p.start()

    # 主进程等待用户输入
    input("主进程等待输入，请按 Enter 键继续...")

    # 结束子进程
    # p.terminate()
    # p.join()
    print("主进程结束。")
