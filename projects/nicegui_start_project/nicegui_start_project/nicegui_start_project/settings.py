from pathlib import Path

from lxml import etree

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
SOURCE_DIR = Path(__file__).resolve().parent.parent

HOST = "localhost"
PORT = 12000
BASE_URL = f"http://{HOST}:{PORT}/"  # NOQA

CONFIGS_PATH = f"{SOURCE_DIR}/conf/configs.xml"
# tree = etree.parse(CONFIGS_PATH)
# root = tree.getroot()
# for child in root.xpath("child"):
#     child_id = child.get("id")
#     child_text = child.text
#     print(f"Child ID: {child_id}, Text: {child_text}")
