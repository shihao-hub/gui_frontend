import io
import os
from pathlib import Path

from nicegui_start_project.utils.file_utils.excel_parser import ExcelCSVConverter

XLSX_FILES_ROOT = r"D:\Software\ToastFish v3.0\Log"
CSV_FILES_POSITION = "./convert_xlsx2csv_resources/csv"

Path(CSV_FILES_POSITION).mkdir(parents=True, exist_ok=True)


def xlsx2csv(filepath: str) -> io.BytesIO:
    res = io.BytesIO()
    xlsx = None

    return res


def main():
    xlsx_files = [f"{XLSX_FILES_ROOT}/{name}" for name in os.listdir(XLSX_FILES_ROOT) if name.endswith(".xlsx")]

    for filepath in xlsx_files:
        filename_no_ext = os.path.splitext(os.path.basename(filepath))[0]
        # ExcelCSVConverter.excel_to_csv(filepath, f"{CSV_FILES_POSITION}/{filename_no_ext}.csv")
        ExcelCSVConverter.csv_to_excel(f"{CSV_FILES_POSITION}/{filename_no_ext}.csv", f"./{filename_no_ext}.xlsx")

        break  # TEST


if __name__ == '__main__':
    main()
