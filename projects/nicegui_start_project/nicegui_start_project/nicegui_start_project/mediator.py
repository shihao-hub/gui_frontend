from typing import Dict, Optional

from lxml import etree

_configs: Optional[Dict] = None


def get_configs(config_file_path: str) -> Dict:
    global _configs

    if _configs is None:
        def _parser_configs_xml_file() -> Dict:
            def cast_value():
                try:
                    if _type is None or _type in {"string"}:  # 默认 string
                        return str(value)
                    elif _type in {"int", "integer"}:
                        return int(value)
                    elif _type in {"bool", "boolean"}:
                        return bool(value)
                    elif _type in {"float", "double"}:
                        return float(value)
                except Exception as e:
                    raise ValueError(f"Cannot cast value: {value} to type: {_type}") from e

                raise ValueError(f"Unknown type: {_type}")

            res = {}
            tree = etree.parse(config_file_path)
            root = tree.getroot()
            for setting in root.xpath("//setting"):
                name = setting.find("name").text
                value = setting.find("value").text
                type_node = setting.find("type")
                # print(type(type_node), type_node)
                _type = type_node if type_node is None else type_node.text
                res[name] = cast_value()
            # print(res)
            return res

        _configs = _parser_configs_xml_file()
    return _configs
