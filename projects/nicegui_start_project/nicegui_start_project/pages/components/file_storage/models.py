import mongoengine as engine

from nicegui_start_project.settings import DATABASE_ALIAS


class File(engine.DynamicDocument):
    filename = engine.StringField(required=True)
    filepath = engine.StringField(required=True)
    filesize = engine.IntField()
    mtime = engine.IntField(default=0)

    meta = dict(collection="file_storage__files", db_alias=DATABASE_ALIAS)

    objects: engine.queryset.queryset.QuerySet
