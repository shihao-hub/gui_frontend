__all__ = [
    "read_html", "read_css", "read_js", "read_sql",
    "read_html_head", "read_html_body"
]

import dataclasses
import enum
import functools
import re
from dataclasses import dataclass
from typing import Literal

import chardet

from .mediator import SingletonMeta

_CACHE_ENABLE = False  # todo: the config of enabling cache


@dataclass
class Row:
    pass


@dataclass
class EnglishRow(Row):
    word: str
    translation: str


class ExcelReader:
    pass


class ReadFileSingleton(metaclass=SingletonMeta()):
    class _FileExtensionEnum(enum.Enum):
        HTML = (enum.auto(), ".html")
        CSS = (enum.auto(), ".css")
        JS = (enum.auto(), ".js")
        SQL = (enum.auto(), ".sql")

        def __init__(self, auto, extension):
            self.auto = auto
            self.extension = extension

    def _check_file_extension(self, filename: str, file_extension: _FileExtensionEnum):
        this = self
        if filename.endswith(file_extension.extension):
            return
        raise ValueError(f"{filename} is not {file_extension.extension} file")

    def _read_text_file(self, filename: str):
        this = self

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

    def _read_file(self, filename: str, mode: str = "r", encoding: str = "utf-8"):
        this = self
        with open(filename, mode, encoding=encoding) as f:
            return f.read()

    def read_html(self, filename: str) -> str:
        self._check_file_extension(filename, self._FileExtensionEnum.HTML)
        return self._read_file(filename)

    def read_css(self, filename: str) -> str:
        self._check_file_extension(filename, self._FileExtensionEnum.CSS)
        return self._read_file(filename)

    def read_js(self, filename: str) -> str:
        self._check_file_extension(filename, self._FileExtensionEnum.JS)
        return self._read_file(filename)

    def read_sql(self, filename: str) -> str:
        self._check_file_extension(filename, self._FileExtensionEnum.SQL)
        return self._read_file(filename)

    def _read_html_tag(self, filename: str, tag_name: Literal["head", "body"]) -> str:
        this = self
        content = read_html(filename)
        pattern = re.compile(rf"<{tag_name}>(.*?)</{tag_name}>", re.DOTALL)
        match = pattern.search(content)
        assert match is not None
        return match.group(1)

    def read_html_head(self, filename: str) -> str:
        return self._read_html_tag(filename, "head")

    def read_html_body(self, filename: str) -> str:
        return self._read_html_tag(filename, "body")


read_html_head = ReadFileSingleton().read_html_head
read_html_body = ReadFileSingleton().read_html_body
read_html = ReadFileSingleton().read_html
read_css = ReadFileSingleton().read_css
read_js = ReadFileSingleton().read_js
read_sql = ReadFileSingleton().read_sql

if _CACHE_ENABLE:
    read_html = functools.cache(read_html)
    read_css = functools.cache(read_css)
    read_js = functools.cache(read_js)
    read_sql = functools.cache(read_sql)
