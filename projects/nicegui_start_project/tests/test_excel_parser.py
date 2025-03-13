import pprint
from dataclasses import dataclass
from . import Row, ExcelReader


@dataclass
class EnglishRow(Row):
    word: str
    translation: str


if __name__ == '__main__':
    reader = ExcelReader(EnglishRow, ["word", "translation"], "./english.xlsx")
    print(pprint.pformat(reader.get_rows()))
