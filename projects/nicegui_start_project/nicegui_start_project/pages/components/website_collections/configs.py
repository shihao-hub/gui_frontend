import collections

PAGE_ICON = "⭐️"
PAGE_TITLE = "网站收藏"
PAGE_PATH = "/pages/components/website_collections"
VERSION = "1.0.0"

HOT_REFRESH = True

_field_names = ["name", "url", "description", "icon", "purpose"]
Website = collections.namedtuple("Website", _field_names)
WEBSITES = [
    Website(
        name="Deepseek 开放平台",
        url="https://platform.deepseek.com",
        description="",
        icon="",
        purpose="主要用于查询 api 用量情况",
    ),
    Website(
        name="金价网",
        url="https://www.jinjia.com.cn/mrjj/",
        description="",
        icon="",
        purpose="主要用于查看每日金价",
    ),
    Website(
        name="如何高效阅读源代码",
        url="https://catcoding.me/p/learn-from-source-code/",
        description="",
        icon="",
        purpose="学习如何高效阅读源代码",
    )
]
