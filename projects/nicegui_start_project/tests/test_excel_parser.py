import inspect
import pprint
from dataclasses import dataclass

from nicegui_start_project.utils.file_utils import excel_parser
from nicegui_start_project.utils.file_utils.excel_parser.interfaces import ExcelRow
from nicegui_start_project.settings import BASE_DIR


@dataclass
class EnglishRow(ExcelRow):
    word: str
    translation: str


if __name__ == '__main__':
    # reader = excel_parser.ExcelReader(f"./english_excel.xlsx", header_var_names=["word", "translation"])
    excel_parser.ExcelCSVConverter.Smoke.test_excel_to_csv()
    excel_parser.ExcelCSVConverter.Smoke.test_csv_to_excel()
