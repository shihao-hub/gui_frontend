__all__ = ["File", "Word"]

import mongoengine as engine

from loguru import logger

DATABASE = "nicegui_start_project"
DATABASE_ALIAS = f"{DATABASE}_alias"

engine.connect(db=DATABASE, alias=DATABASE_ALIAS, host="localhost", port=27017)


class File(engine.DynamicDocument):
    filename = engine.StringField(required=True)
    filepath = engine.StringField(required=True)
    filesize = engine.IntField()

    meta = dict(collection="files", db_alias=DATABASE_ALIAS)

    objects: engine.queryset.queryset.QuerySet


class Word(engine.DynamicDocument):
    word = engine.StringField(required=True, unique=True)  # unique=True -> NotUniqueError
    meaning = engine.StringField(required=True)

    meta = dict(collection="word_notebook__words", db_alias=DATABASE_ALIAS)
    objects: engine.queryset.queryset.QuerySet

    def clean(self):
        def clean_field_tear_down(field_name):
            def decorator(func):
                def wrapper(*args, **kwargs):
                    old_value = getattr(self, field_name, None)
                    try:
                        return func(*args, **kwargs)
                    except engine.ValidationError as e:
                        raise e
                    except Exception as e:
                        logger.error(f"{e}")
                        if hasattr(self, field_name):
                            setattr(self, field_name, old_value)

                return wrapper

            return decorator

        @clean_field_tear_down("word")
        def iife_clean_word():
            word = self.word.strip()
            print(word)
            # check that the word field is for words
            # if word.isalpha():
            #     self.word = word
            # self.word = "aaa"
            # raise engine.ValidationError("Word field must contain only letters")

        iife_clean_word()


if __name__ == '__main__':
    def test_Word():  # NOQA
        Word.drop_collection()
        word = Word(word="hello", meaning="world")
        word.save()
