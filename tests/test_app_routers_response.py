import pprint
import threading
from typing import Dict
from uuid import uuid4

import aiohttp
import requests
from nicegui import ui, app


class shared_client_data:  # NOQA
    locals: Dict[str, Dict] = {}


# @ui.page("/")
def index():
    client_id = str(uuid4())

    print(pprint.pformat([e.path for e in app.routes]))

    @app.get("/hello")
    async def hello():
        local = shared_client_data.locals[client_id]
        label = local.get("label")

        print(f"label id: {id(label)}")
        label.set_text(client_id)

    async def on_click():
        print(123, flush=True)
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:10086/hello") as response:
                print(response)

    label = ui.label()
    print(f"label id: {id(label)}")
    button = ui.button("Click me", on_click=on_click)

    shared_client_data.locals[client_id] = locals()

    print(pprint.pformat([e.path for e in app.routes]))

    print()
    print()


print(threading.current_thread())
index()
ui.run(host="localhost", port=10086, reload=False, show=False)
