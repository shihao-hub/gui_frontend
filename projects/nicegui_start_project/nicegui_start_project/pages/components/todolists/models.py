import mongoengine as engine

from nicegui_start_project.settings import DATABASE_ALIAS


class TodoList(engine.DynamicDocument):
    index = engine.IntField(required=True)
    content = engine.StringField(required=True)

    meta = dict(collection="todolists__todolists", db_alias=DATABASE_ALIAS)

    objects: engine.queryset.queryset.QuerySet
