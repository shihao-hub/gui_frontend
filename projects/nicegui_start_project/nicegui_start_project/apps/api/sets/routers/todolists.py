from fastapi import APIRouter

router = APIRouter(prefix="/todolists", tags=["todolists"])


# class ApiMixin:
#     @staticmethod
#     async def create():
#         pass
#
#     @staticmethod
#     async def read():
#         pass
#
#     @staticmethod
#     async def update():
#         pass
#
#     @staticmethod
#     async def delete():
#         pass
#
#     @staticmethod
#     async def list():
#         pass


class TodoLists:
    @staticmethod
    @router.post("")
    async def create():
        pass

    @staticmethod
    @router.get("/{id}")
    async def read(self):
        pass

    @staticmethod
    @router.put("/{id}")
    async def update(self):
        pass

    @staticmethod
    @router.delete("/{id}")
    async def delete(self):
        pass

    @staticmethod
    @router.get("")
    async def list():
        return 200, {"data": [1]}
