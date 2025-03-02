from typing import TypedDict

import mongoengine as engine
from pydantic import BaseModel

from nicegui_start_project.settings import DATABASE_ALIAS


class TodoListTypedDict(TypedDict):
    uid: str
    task: str
    done: bool


class TodoListSchema(BaseModel):
    uid: str
    task: str
    done: bool = False

    @classmethod
    def create(cls, uid: str, task: str, done: bool = False) -> "TodoListSchema":
        return cls(uid=uid, task=task, done=done)


class TodoList(engine.DynamicDocument):
    """ 负责数据管理和业务逻辑，不依赖 NiceGUI。 """
    task = engine.StringField(required=True)
    done = engine.BooleanField(default=False)

    meta = dict(collection="todolists__todolists", db_alias=DATABASE_ALIAS)

    objects: engine.queryset.queryset.QuerySet
