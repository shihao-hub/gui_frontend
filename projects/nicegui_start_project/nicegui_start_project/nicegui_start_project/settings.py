import sqlite3
from pathlib import Path

import pymongo
import redis

from .mediator import get_configs

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SOURCE_DIR = Path(__file__).resolve().parent.parent

# 最初计划整个项目使用 mongodb 的，因此命名为 DATABASE。但是现在发现，关系表值得一试，比如 sqlalchemy 库！
DATABASE = "nicegui_start_project"
DATABASE_ALIAS = f"{DATABASE}_alias"

CONFIG_FILE_PATH = f"{BASE_DIR}/conf/configs.xml"

# 原始 redis, mongodb, sqlite ... 其中 sqlite 最省事，因为是文件数据库
redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
mongodb_db = pymongo.MongoClient("mongodb://localhost:27017/").get_database("0")
sqlite_db = sqlite3.connect(f"{SOURCE_DIR}/sqlite3.db")

configs = get_configs(CONFIG_FILE_PATH)

HOST = configs.get("HOST")
PORT = configs.get("PORT")
BASE_URL = f"http://{HOST}:{PORT}/"  # NOQA

NFS_SERVICE_STARTUP_ENTRY_PATH = f"{BASE_DIR}/services/nfs_service/nfs/main.py"
COMPONENTS_ROOT_DIR = f"{SOURCE_DIR}/pages/components"
COMPONENTS_PACKAGE_NAME = "pages.components"
