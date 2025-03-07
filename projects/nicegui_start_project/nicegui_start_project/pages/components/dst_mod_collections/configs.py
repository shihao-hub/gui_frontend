from dataclasses import dataclass
from typing import List

PAGE_ICON = "⚔️"
PAGE_TITLE = "饥荒模组合集"
PAGE_PATH = "/pages/components/dst_mod_collections"
VERSION = ""


@dataclass
class ModInfo:
    name: str
    brief_desc: str
    icon: str
    tags: List[str]


MODS_INFO = [
    ModInfo(
        name="更多物品",
        brief_desc="很多物品",
        icon="",
        tags=["容器", "食物"],
    ),
]
