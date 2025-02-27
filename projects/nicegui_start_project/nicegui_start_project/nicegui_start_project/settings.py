from pathlib import Path

import pymongo
import redis

from .mediator import get_configs

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SOURCE_DIR = Path(__file__).resolve().parent.parent

DATABASE = "nicegui_start_project"
DATABASE_ALIAS = f"{DATABASE}_alias"

CONFIG_FILE_PATH = f"{BASE_DIR}/conf/configs.xml"

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
mongodb_db = pymongo.MongoClient("mongodb://localhost:27017/").get_database("0")

configs = get_configs(CONFIG_FILE_PATH)

HOST = configs.get("HOST")
PORT = configs.get("PORT")
BASE_URL = f"http://{HOST}:{PORT}/"  # NOQA

NFS_SERVICE_STARTUP_ENTRY_PATH = f"{BASE_DIR}/services/nfs_service/nfs/main.py"
COMPONENTS_ROOT_DIR = f"{SOURCE_DIR}/pages/components"
COMPONENTS_PACKAGE_NAME = "pages.components"
