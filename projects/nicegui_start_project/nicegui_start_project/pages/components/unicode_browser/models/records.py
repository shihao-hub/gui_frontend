"""
纯数据载体，无业务逻辑
"""

from dataclasses import dataclass, asdict


@dataclass
class UserRecord:
    name: str
    password: str
