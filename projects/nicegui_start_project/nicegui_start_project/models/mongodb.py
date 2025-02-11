import mongoengine as engine

DATABASE = "nicegui_start_project"
DATABASE_ALIAS = f"{DATABASE}_alias"

engine.connect(db=DATABASE, alias=DATABASE_ALIAS, host="localhost", port=27017)


class File(engine.DynamicDocument):
    filename = engine.StringField(required=True)
    filepath = engine.StringField(required=True)
    filesize = engine.IntField()

    meta = dict(collection="files", db_alias=DATABASE_ALIAS)

    objects: engine.queryset.queryset.QuerySet


if __name__ == '__main__':
    print(type(File.objects))
