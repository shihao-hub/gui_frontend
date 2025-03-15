import mongoengine as engine

from nicegui_start_project.utils import get_mongonengine_meta, SingletonMeta, MongoAPIService


class UnicodeEntity(engine.DynamicDocument):
    char = engine.StringField(required=True)
    code = engine.StringField(required=True)
    name = engine.StringField(required=True)

    meta = get_mongonengine_meta("unicode_browser__unicodes")
    objects: engine.queryset.queryset.QuerySet

    class Service(MongoAPIService["Unicode"], metaclass=SingletonMeta):
        """服务类 | 业务逻辑处理类"""
        def __init__(self):
            super().__init__(UnicodeEntity)


class UnicodeTranslationEntity(engine.DynamicDocument):
    english_name = engine.StringField(required=True)
    chinese_name = engine.StringField(required=True)

    meta = get_mongonengine_meta("unicode_browser__unicode_translations")
    objects: engine.queryset.queryset.QuerySet
