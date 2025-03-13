import io
import os

XLSX_FILES_ROOT = r"D:\Software\ToastFish v3.0\Log"
CSV_FILES_POSITION = "./convert_xlsx2csv_resources/csv"


def xlsx2csv(filepath: str) -> io.BytesIO:
    res = io.BytesIO()
    xlsx = None

    return res


def main():
    xlsx_files = [f"{XLSX_FILES_ROOT}/{name}" for name in os.listdir(XLSX_FILES_ROOT) if name.endswith(".xlsx")]

    for filepath in xlsx_files:
        csv = xlsx2csv(filepath)
        # todo: 路径上的文件夹不存在都给创建出来！
        break  # TEST


if __name__ == '__main__':
    main()
