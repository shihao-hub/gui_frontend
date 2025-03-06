import sqlite3
from pathlib import Path
from typing import Optional

import pymongo
import redis
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .mediator import get_configs

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SOURCE_DIR = Path(__file__).resolve().parent.parent
SQLITE_DB_PATH = f"{SOURCE_DIR}/sqlite3.db"

# 最初计划整个项目使用 mongodb 的，因此命名为 DATABASE。但是现在发现，关系表值得一试，比如 sqlalchemy 库！
DATABASE = "nicegui_start_project"
DATABASE_ALIAS = f"{DATABASE}_alias"

CONFIG_FILE_PATH = f"{BASE_DIR}/conf/configs.xml"

configs = get_configs(CONFIG_FILE_PATH)

HOST = configs.get("HOST")
PORT = configs.get("PORT")
BASE_URL = f"http://{HOST}:{PORT}/"  # NOQA

NFS_SERVICE_STARTUP_ENTRY_PATH = f"{BASE_DIR}/services/nfs_service/nfs/main.py"
COMPONENTS_ROOT_DIR = f"{SOURCE_DIR}/pages/components"
COMPONENTS_PACKAGE_NAME = "pages.components"


class _DatabaseManager:
    """优化成懒加载"""

    def __init__(self):
        self._sqlite_db: Optional[sqlite3.Connection] = None  # sqlite 最省事，因为是文件数据库
        self._mongodb_db: Optional[pymongo.MongoClient] = None
        self._redis_db: Optional[redis.StrictRedis] = None

        self._sqlalchemy_engine: Optional[sqlalchemy.Engine] = None
        self._SqlAlchemySession: Optional[sqlalchemy.sessionmaker] = None

    @property
    def sqlite_db(self):
        if self._sqlite_db is None:
            self._sqlite_db = sqlite3.connect(f"{SQLITE_DB_PATH}")
        return self._sqlite_db

    @property
    def mongodb_db(self):
        if self._mongodb_db is None:
            self._mongodb_db = pymongo.MongoClient("mongodb://localhost:27017/").get_database("0")
        return self._mongodb_db

    @property
    def redis_db(self):
        if self._redis_db is None:
            self._redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
        return self._redis_db

    def _get_sqlalchemy_engine(self):
        if self._sqlalchemy_engine is None:
            self._sqlalchemy_engine = create_engine(f"sqlite:///{SQLITE_DB_PATH}")
        return self._sqlalchemy_engine

    @property
    def sqlalchemy_engine(self):
        return self._get_sqlalchemy_engine()

    @property
    def SqlAlchemySession(self):  # NOQA
        if self._SqlAlchemySession is None:
            self._SqlAlchemySession = sessionmaker(bind=self._get_sqlalchemy_engine())
        return self._SqlAlchemySession

    # def create_(self):


database_manager = _DatabaseManager()
