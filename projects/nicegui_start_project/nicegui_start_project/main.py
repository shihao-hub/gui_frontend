import importlib
from typing import List

from nicegui import ui

from pages import components
from nicegui_start_project.settings import HOST, PORT, BASE_URL
from apps.api.routers import register_routers

# importlib.import_module("projects.nicegui_start_project.src.pages.components.todolists.todolists")

register_routers()


def url_join(snippets: List[str]) -> str:
    return "/".join([e.strip("/") for e in snippets])


def main():
    with ui.column():
        for name in dir(components):
            if name.startswith("_"):
                continue
            module = getattr(components, name)
            if hasattr(module, "PAGE_TITLE") and hasattr(module, "PAGE_PATH"):
                link = ui.link(getattr(module, "PAGE_TITLE"), url_join([BASE_URL, getattr(module, "PAGE_PATH")]))
                link.props(""" target="_blank" """)


if __name__ == '__main__':
    main()
    ui.run(host=HOST, port=PORT, reload=False, show=False, favicon="🚀")
