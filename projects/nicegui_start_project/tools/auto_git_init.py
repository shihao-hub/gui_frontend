"""
### 需求分析
- 从下载目录找到 gui_frontend_main{int} 最新的压缩包，解压缩并移动到指定目录
- 执行 git init 和 git_push.bat 命令

"""
import functools
import json
import re
import datetime
import os
import shutil
import subprocess
import threading
import time
import zipfile
from pathlib import Path
from typing import Tuple, Dict, Literal

from loguru import logger
from tqdm import tqdm

DOWNLOAD_DIR = r"C:\Users\z30072623\Downloads"
FILENAME_PREFIX = "gui_frontend-main"
TARGET_DIR = r"D:\GithubCodes\PyCharm-gui_frontend-main"


def print_error_info(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"❌ Error occurred in {func.__name__}: {e}")

    return wrapper


def _get_latest_file_id(pwd: str, pattern, file_type: Literal["file", "dir"]) -> int:
    # 2 usages，存在重复代码，因此提取出来，但是这提取出来的并没有正面意义吧？
    res = -1
    for name in os.listdir(pwd):
        path = Path(pwd) / name
        match = pattern.match(path.name)
        is_target_file = path.is_file() if file_type == "file" else path.is_dir()
        if is_target_file and match:
            res = max(res, int(match.group(1)))
    assert res != -1
    return res


def _get_download_zip_file() -> str:
    """获得需要解压缩的那个文件的路径"""
    max_num = _get_latest_file_id(DOWNLOAD_DIR, re.compile(rf"{FILENAME_PREFIX} \((\d+)\).zip"), "file")
    assert max_num != -1
    res = Path(DOWNLOAD_DIR) / f"{FILENAME_PREFIX} ({max_num}).zip"
    logger.info(f"download zip file: {res}")
    return str(res)


def _decompress_with_progress_bar(zip_ref, target_filepath):
    file_list = zip_ref.namelist()
    with tqdm(total=len(file_list), unit="file", desc="Extracting") as pbar:
        for file in file_list:
            zip_ref.extract(file, target_filepath)
            pbar.update(1)  # 每解压一个文件，进度条+1


def decompress_file() -> str:

    # flow: 获得最新的那个文件，这个最新是指 id 的最大值
    max_num = _get_latest_file_id(TARGET_DIR, re.compile(rf"{FILENAME_PREFIX}(\d+)"), "dir")
    target_filename = f"{FILENAME_PREFIX}{max_num + 1}"
    logger.info(f"target filename: {target_filename}")
    target_filepath = str(Path(TARGET_DIR) / target_filename)

    # flow: 添加校验，如果最新的那个目录的创建时间距离当前时间太近，则需要用户决定
    latest_filepath = Path(TARGET_DIR) / f"{FILENAME_PREFIX}{max_num}"
    stat_info = os.stat(latest_filepath)
    created_time = stat_info.st_ctime
    logger.info(f"created time: {datetime.datetime.fromtimestamp(created_time)}")
    interval = 60
    if time.time() - created_time < 60:
        ipt = input(f"最新目录的创建时间距离当前时间太近（少于 {interval} 秒），是否继续？(y/n)\n")
        if ipt == "n":
            raise Exception("用户选择不继续")

    # flow: extractall 会将 a (1).zip 双击打开显示的内容复制到其第一个参数 path 代表的目录中
    download_file = _get_download_zip_file()
    with zipfile.ZipFile(download_file, "r") as zip_ref:
        # _decompress_with_progress_bar(zip_ref, target_filepath)
        zip_ref.extractall(target_filepath)
    logger.info("decompress file successfully.")

    # flow: 将提取出来的文件最外层目录剥离掉
    files = os.listdir(target_filepath)
    assert len(files) == 1
    for name in files:
        path = Path(target_filepath) / name
        assert path.is_dir()
        for src_path in path.iterdir():
            shutil.move(src_path, target_filepath)
        shutil.rmtree(path)

    return target_filepath


@print_error_info
def run_git_init(pwd: str):
    result = subprocess.run(
        ["git", "init"],
        cwd=pwd,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True  # 确保输出为字符串（Python 3.7+）
    )
    logger.info(f"git init result: {result.stdout}")


@print_error_info
def run_git_push(pwd: str):
    logger.info("start running git_push.bat")
    result = subprocess.run(
        ["git_push.bat"],  # 直接运行 BAT 文件
        cwd=pwd,  # 指定工作目录
        shell=True,
        check=True,  # 检查命令是否成功
        stdout=subprocess.PIPE,  # 捕获标准输出
        stderr=subprocess.PIPE,  # 捕获错误输出
        input=b"\n",  # 因为 bat 中的 pause 居然会暂停主进程，所以设置自动发送回车键
    )
    # \r\n\xc7\xeb\xb0\xb4\xc8\xce\xd2\xe2\xbc\xfc\xbc\xcc\xd0\xf8
    # logger.info(f"git_push.bat result:\n {result.stdout}")
    if result.returncode != 0:
        logger.error(f"git_push.bat error:\n {result.stderr}")


def output(arguments: Dict):
    logger.info("output: " + json.dumps(arguments, ensure_ascii=False, indent=4))


def main():
    """
    graph TD
    A[开始] --> B[解压到指定目录，命名需要 id 递增]
    B --> C[进入目录，使用 cmd 执行 git init]
    C --> D[执行完毕后，使用 cmd 运行 git_push.bat 文件]
    D --> E[运行完毕，输出目标所在位置]

    """
    s = time.time()

    target_filepath = decompress_file()
    run_git_init(target_filepath)
    run_git_push(target_filepath)
    output({"target_filepath": target_filepath})

    logger.info(f"total time: {time.time() - s:.4f}s")


if __name__ == '__main__':
    main()
