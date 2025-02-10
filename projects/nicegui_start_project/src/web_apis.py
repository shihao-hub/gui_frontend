__all__ = [
    "get_users"
]

from typing import Dict, TypedDict

from pydantic import BaseModel


# 这个能不能这样？直接用 Schema/BaseModel 充当对象，实例化并校验和传递
class GetUsersBodySchema(BaseModel):
    pass


class GetUsersBody(TypedDict):
    pass


def get_users(body: GetUsersBody):
    pass
