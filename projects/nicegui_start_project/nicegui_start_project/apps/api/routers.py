__all__ = ["register_routers"]

import importlib
import pprint
from typing import Callable

from nicegui import app
from fastapi.routing import APIRoute


def register_routers():
    # note: 框架开发大部分应该都是这样的吧？我发现我更喜欢这样，尤其如何团队有一些大佬，那就可以快速学习。（我需要离开这里）
    module = importlib.import_module("apps.api.sets.routers")

    for name in dir(module):
        if name.endswith("_router"):
            router = getattr(module, name)
            app.include_router(router, prefix="/api", tags=["api"])
    print(pprint.pformat([f"{e.path} - {e.methods}" for e in app.routes if isinstance(e, APIRoute)]))
