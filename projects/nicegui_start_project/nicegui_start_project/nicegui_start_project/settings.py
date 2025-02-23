from pathlib import Path
from typing import Dict

import redis
from lxml import etree

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SOURCE_DIR = Path(__file__).resolve().parent.parent

DATABASE = "nicegui_start_project"
DATABASE_ALIAS = f"{DATABASE}_alias"

CONFIGS_PATH = f"{BASE_DIR}/conf/configs.xml"

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)


def iife_parser_configs_xml_file() -> Dict:
    def cast_value():
        try:
            if type_alias is None:
                return str(value)
            elif type_alias in {"int", "integer"}:
                return int(value)
            elif type_alias in {"bool", "boolean"}:
                return bool(value)
            elif type_alias in {"float", "double"}:
                return float(value)
        except Exception as e:
            raise ValueError(f"Cannot cast value: {value} to type: {type_alias}") from e

        raise ValueError(f"Unknown type: {type_alias}")

    res = {}
    tree = etree.parse(CONFIGS_PATH)
    root = tree.getroot()
    for setting in root.xpath("//setting"):
        name = setting.find("name").text
        value = setting.find("value").text
        type_node = setting.find("type")
        print(type(type_node), type_node)
        type_alias = type_node if type_node is None else type_node.text
        res[name] = cast_value()
    # print(res)
    return res


configs: Dict = iife_parser_configs_xml_file()

HOST = configs.get("HOST")
PORT = configs.get("PORT")
BASE_URL = f"http://{HOST}:{PORT}/"  # NOQA


def update_configs(settings_alias: Dict):
    configs.update(settings_alias)

    tree = etree.parse(CONFIGS_PATH)
    root = tree.getroot()
    settings_element = root.find("settings")
    settings_element.clear()

    # 添加新的配置项
    for name, value in configs.items():
        setting = etree.Element("setting")
        name_elem = etree.Element("name")
        name_elem.text = name
        value_elem = etree.Element("value")
        value_elem.text = str(value)
        setting.append(name_elem)
        setting.append(value_elem)
        settings_element.append(setting)

    tree.write(CONFIGS_PATH, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    print("Update configs success!")
