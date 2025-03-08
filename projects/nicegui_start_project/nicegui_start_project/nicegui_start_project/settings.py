import contextlib
import sqlite3
from pathlib import Path
from typing import Optional, Type, Generator, ContextManager

import pymongo
import redis
import sqlalchemy
from sqlalchemy import create_engine, Engine as SqlAlchemyEngine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.session import Session as SqlAlchemySession
from sqlalchemy.orm.decl_api import DeclarativeMeta as SqlAlchemyDeclarativeMeta

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

    # ========================================
    # make lazy loading to avoid slow startup?
    # ========================================
    class _Sqlalchemy:
        def __init__(self):
            self._engine: Optional[SqlAlchemyEngine] = None
            self._Base: Optional[Type[SqlAlchemyDeclarativeMeta]] = None
            self._Session: Optional[Type[SqlAlchemySession]] = None

        def _get_engine(self):
            if self._engine is None:
                self._engine = create_engine(f"sqlite:///{SQLITE_DB_PATH}")
            return self._engine

        @property
        def engine(self):
            return self._get_engine()

        @property
        def Session(self):  # NOQA
            if self._Session is None:
                self._Session = sessionmaker(bind=self._get_engine())
            return self._Session

        @property
        def Base(self):  # NOQA
            if self._Base is None:
                self._Base = declarative_base()
            return self._Base

        @contextlib.contextmanager
        def session_scope(self) -> ContextManager[SqlAlchemySession]:
            """Provide a transactional scope around a series of operations."""
            session: SqlAlchemySession = self.Session()
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()

        def create_all(self):
            self.Base.metadata.create_all(self.engine)

    def __init__(self):
        self._sqlite_db: Optional[sqlite3.Connection] = None  # sqlite 最省事，因为是文件数据库
        self._mongodb_db: Optional[pymongo.MongoClient] = None
        self._redis_db: Optional[redis.StrictRedis] = None

        self.sqlalchemy = self._Sqlalchemy()

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


database_manager = _DatabaseManager()
