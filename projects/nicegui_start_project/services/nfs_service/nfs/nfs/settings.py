import configparser
from pathlib import Path
from typing import Optional, Any

from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
NFS_BASE_DIR = Path(__file__).parent.parent.parent
NFS_SOURCE_DIR = Path(__file__).parent.parent


class _Configs:
    config_file = f"{BASE_DIR}/conf/services.ini"

    def __init__(self, config_file: str = None):
        self.configs = configparser.ConfigParser()
        self.configs.read(self.config_file if config_file is None else config_file)

        self.section = "nfs_service"

    def get(self, key: str) -> Any:
        if not self.configs.has_option("nfs_service", key):  # configparser.NoOptionError，不选择 try except 了，而是先验
            logger.warning(f"配置文件中未找到配置项：{key}")
            return None

        res = self.configs.get("nfs_service", key)

        assert isinstance(res, str)

        flag_position = res.rfind(":")
        if flag_position == -1:
            return res

        # 出现形如 value:type 的结构时，会尝试自动 cast
        res_value = res[:flag_position].strip()
        res_type = res[flag_position + 1:].strip()
        if res_type == "int":
            return int(res_value)
        elif res_type == "float":
            return float(res_value)
        elif res_type == "bool":
            return bool(res_value)

        return res


configs = _Configs()
