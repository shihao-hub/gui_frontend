import argparse
import re
import subprocess
import sys
import threading
from pathlib import Path

from loguru import logger

PWD = Path(__file__).resolve().parent
SCRIPTS_DIR = Path(sys.executable).resolve().parent


def get_filepath() -> str:
    # parser = argparse.ArgumentParser()
    # parser.add_argument("fp", type=str, help="file path")
    # args = parser.parse_args()
    # res = args.fp
    res = input("input filepath: (absolute path or relative path)\n")
    res = res.strip()
    if not re.match("[A-Za-z]:", res):
        res = str(PWD / res)
    if not Path(res).exists():
        raise FileNotFoundError(res)
    return res


def run_command(filepath: str):
    # pyinstaller -F filepath
    process = subprocess.Popen(
        ["cmd", "/c", f"{SCRIPTS_DIR / "pyinstaller.exe"}", "-F", f"{filepath}"],  # 显式调用 cmd
        cwd=str(PWD),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,  # 自动解码输出
        encoding="utf-8",
        errors="replace",  # 处理解码错误
        bufsize=1,  # 行缓冲模式！
    )
    logger.info("process has been started, now capturing the output...")

    # 实时读取输出流的工具函数
    def stream_reader(stream, is_error=False):
        for line in iter(stream.readline, ''):
            line = line.rstrip()
            if line:
                if is_error:
                    logger.error(f"[STDERR] {line}")
                else:
                    logger.info(f"[STDOUT] {line}")
        stream.close()

    # 启动线程读取输出（或使用异步库处理）
    # 此处简化使用同步读取（适合快速输出的场景）
    stdout_thread = threading.Thread(target=stream_reader, args=(process.stdout, False))
    # Q: 为什么输出都是 stderr 而 stdout 无内容
    stderr_thread = threading.Thread(target=stream_reader, args=(process.stderr, True))

    stdout_thread.start()
    stderr_thread.start()

    # 等待进程结束或超时
    process.wait(timeout=300)

    # 等待输出线程结束
    stdout_thread.join(timeout=1)
    stderr_thread.join(timeout=1)

    # 检查返回码
    if process.returncode != 0:
        logger.error(f"进程异常结束，返回码: {process.returncode}")
    else:
        logger.info("操作成功完成")


def main():
    """
    # 输入文件路径，如果文件路径起始是 x: 则视为绝对路径，否则视为相对路径
    # 通过 cmd 执行 pyinstaller 打包，注意这个 pyinstaller 属于某个虚拟环境
    """

    filepath = get_filepath()
    run_command(filepath)


if __name__ == '__main__':
    main()
