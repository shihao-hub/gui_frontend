__all__ = [
    "read_html", "read_css", "read_js",
    "read_html_head", "read_html_body"
]

import re
from typing import Literal

import chardet


def read_text_file(filename: str):
    # check_text_file
    # probe_file_coding
    # read_file
    def check_text_file():
        extensions = {}

    def read_file():
        with open(filename, "rb") as f:
            raw_data = f.read()
        encoding = chardet.detect(raw_data).get("encoding")
        assert encoding is not None
        return raw_data.decode(encoding)

    check_text_file()
    return read_file()


# todo: cache 对接 redis（当然，还需要遵循 如非必要，勿增实体 的原则）
# note: 注释掉的话，html 就可以视为配置文件了，刷新而不需要重启就可以更新 html 内容！
# @functools.cache
def read_html(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def read_css(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def read_js(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def _read_html_tag(filename: str, tag_name: Literal["head", "body"]) -> str:
    content = read_html(filename)
    pattern = re.compile(rf"<{tag_name}>(.*?)</{tag_name}>", re.DOTALL)
    match = pattern.search(content)
    assert match is not None
    return match.group(1)


def read_html_head(filename: str) -> str:
    return _read_html_tag(filename, "head")


def read_html_body(filename: str) -> str:
    return _read_html_tag(filename, "body")
