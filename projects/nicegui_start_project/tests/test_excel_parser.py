import pprint
from dataclasses import dataclass

from nicegui_start_project.utils.file_utils import excel_parser
from nicegui_start_project.settings import BASE_DIR


@dataclass
class EnglishRow(excel_parser.Row):
    word: str
    translation: str


if __name__ == '__main__':
    reader = excel_parser.ExcelReader(EnglishRow, ["word", "translation"], f"./english_excel.xlsx")
    print(pprint.pformat(reader.get_rows()))
