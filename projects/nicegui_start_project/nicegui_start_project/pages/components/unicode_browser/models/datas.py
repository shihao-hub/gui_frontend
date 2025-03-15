"""
纯数据载体，无业务逻辑
"""

from dataclasses import dataclass, asdict


@dataclass
class UserData:
    name: str
    password: str
