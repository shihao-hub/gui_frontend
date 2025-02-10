import importlib
from typing import List

from nicegui import ui
from projects.nicegui_start_project.src.pages import components

# importlib.import_module("projects.nicegui_start_project.src.pages.components.todolists.todolists")

HOST = "localhost"
PORT = 12000
BASE_URL = f"http://{HOST}:{PORT}/"  # NOQA


def url_join(snippets: List[str]) -> str:
    return "/".join([e.strip("/") for e in snippets])


def main():
    with ui.column():
        for name in dir(components):
            if name.startswith("_"):
                continue
            module = getattr(components, name)
            if hasattr(module, "PAGE_TITLE") and hasattr(module, "PAGE_PATH"):
                ui.link(getattr(module, "PAGE_TITLE"), url_join([BASE_URL, getattr(module, "PAGE_PATH")]))


if __name__ == '__main__':
    main()
    ui.run(host=HOST, port=PORT, reload=False, show=False)
