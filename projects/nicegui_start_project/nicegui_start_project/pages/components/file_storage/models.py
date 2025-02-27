from typing import List

import mongoengine as engine

from nicegui_start_project.settings import DATABASE_ALIAS
from nicegui_start_project.utils import sync_to_async


class File(engine.DynamicDocument):
    filename = engine.StringField(required=True)
    filepath = engine.StringField(required=True)
    filesize = engine.IntField()
    mtime = engine.IntField(default=0)

    meta = dict(collection="file_storage__files", db_alias=DATABASE_ALIAS)

    objects: engine.queryset.queryset.QuerySet

    # DAO 层
    @classmethod
    async def create(cls, **kwargs) -> "File":
        return await sync_to_async(lambda: cls.objects.create(**kwargs))

    @classmethod
    async def delete(cls, **kwargs) -> "File":
        return await sync_to_async(lambda: cls.objects(**kwargs).delete())

    @classmethod
    async def get_all(cls) -> List["File"]:
        return await sync_to_async(lambda: cls.objects.all())
