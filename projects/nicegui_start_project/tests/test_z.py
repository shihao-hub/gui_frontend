import collections
from dataclasses import dataclass, asdict, astuple, make_dataclass, is_dataclass


# @dataclass
# class FileInfo:
#     filename: str
#     content: str


FileInfo = collections.namedtuple("FileInfo", ["filename", "content"])
# print(type(FileInfo))

# FileInfo = make_dataclass("FileInfo", [("filename", str), ("content", str)])


file_infos = [
    FileInfo(
        filename="__init__.py",
        content="""\
from .entities import *
"""
    ),

]

info = file_infos[0]
info.filename = 1
print(info)
