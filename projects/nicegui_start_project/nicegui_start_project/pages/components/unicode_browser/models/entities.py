import mongoengine as engine

from nicegui_start_project.utils import get_mongonengine_meta, SingletonMeta, APIService


class UnicodeEntity(engine.DynamicDocument):
    char = engine.StringField(required=True)
    code = engine.StringField(required=True)
    name = engine.StringField(required=True)

    meta = get_mongonengine_meta("unicode_browser__unicodes")
    objects: engine.queryset.queryset.QuerySet

    class Service(APIService["Unicode"], metaclass=SingletonMeta):
        """服务类 | 业务逻辑处理类"""
        def __init__(self):
            super().__init__(UnicodeEntity)


class UnicodeTranslation(engine.DynamicDocument):
    english_name = engine.StringField(required=True)
    chinese_name = engine.StringField(required=True)

    meta = get_mongonengine_meta("unicode_browser__unicode_translations")
    objects: engine.queryset.queryset.QuerySet
