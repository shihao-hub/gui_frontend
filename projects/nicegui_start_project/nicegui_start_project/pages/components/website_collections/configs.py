import collections

PAGE_ICON = "⭐️"
PAGE_TITLE = "网站收藏"
PAGE_PATH = "/pages/components/website_collections"
VERSION = "1.0.0"

_field_names = ["name", "url", "description", "icon", "purpose"]
Website = collections.namedtuple("Website", _field_names)
WEBSITES = [
    Website(
        name="Deepseek 开放平台",
        url="https://platform.deepseek.com",
        description="",
        icon="",
        purpose="主要用于查询 api 用量情况",
    )
]
