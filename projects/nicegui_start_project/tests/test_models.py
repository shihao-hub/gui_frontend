import time

import mongoengine as engine

from nicegui_start_project.settings import DATABASE, DATABASE_ALIAS
from pages.components.unicode_browser.models import UnicodeEntity as Unicode

engine.connect(db=DATABASE, alias=DATABASE_ALIAS, host="localhost", port=27017)

inst = Unicode.Service().create(**dict(char="aaaaa", code="67", name="a"))
print(inst.to_mongo().to_dict())
print(Unicode.Service().get(inst.id))
print(Unicode.Service().lists())
