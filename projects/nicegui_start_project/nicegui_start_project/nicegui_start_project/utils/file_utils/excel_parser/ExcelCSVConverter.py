import csv

import pandas as pd
from loguru import logger

from .interfaces.FileConverter import FileConverter
from ._mediator import var_ExcelReader

ExcelReader = var_ExcelReader()


# todo: 熟练使用 pandas

class ExcelCSVConverter(FileConverter):
    @staticmethod
    def _check_file_type(excel_file: str, csv_file: str):
        if excel_file.endswith(".xlsx") and csv_file.endswith(".csv"):
            return
        raise ValueError("文件类型不匹配，请检查文件扩展名。")

    @staticmethod
    def excel_to_csv(excel_file: str, csv_file: str):
        # 将 Excel 数据导入内存，获得所有行数据
        # 将这些数据转为 csv 文件

        ExcelCSVConverter._check_file_type(excel_file, csv_file)

        reader = ExcelReader(excel_file)
        rows = reader.get_rows(min_row=1)

        with open(csv_file, "w", newline="", encoding="utf-8") as outfile:
            csv_writer = csv.writer(outfile)
            csv_writer.writerows(rows)
        logger.info(f"Excel 文件已转换为 CSV 文件: {csv_file}")

    @staticmethod
    def csv_to_excel(csv_file: str, excel_file: str):
        # 将 csv 数据导入内存，获得所有行数据
        # 将这些数据转为 Excel 文件

        ExcelCSVConverter._check_file_type(excel_file, csv_file)

        df = pd.read_csv(csv_file)
        df.to_excel(excel_file, index=False)
        logger.info(f"CSV 文件已转换为 Excel 文件: {excel_file}")

    class Smoke:
        @staticmethod
        def test_excel_to_csv():
            converter = ExcelCSVConverter()
            converter.excel_to_csv(f"./english_excel.xlsx", f"./english_excel.csv")

        @staticmethod
        def test_csv_to_excel():
            converter = ExcelCSVConverter()
            converter.csv_to_excel(f"./english_excel.csv", f"./english_excel2.xlsx")
