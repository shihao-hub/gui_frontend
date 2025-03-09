import re
from typing import List

from nicegui import app
from fastapi import Form, HTTPException, status
from fastapi.requests import Request

from nicegui_start_project.settings import database_manager
from .. import configs

TODO_LIST_KEY = "api:redis:todo_list"
BASE_URL = f"{configs.PAGE_PATH}/api/redis/todolists"

db = database_manager.redis_db


def _check_index(index: int, list_len: int = None):
    if list_len is None:
        list_len = db.llen(TODO_LIST_KEY)

    # check the index range
    if index < 0 or index >= list_len:
        raise HTTPException(status_code=400, detail="Out of index range")


def _remove_element_by_index(index: int):
    # lua script：使用 lrange 找出不需要删除的元素，然后将旧列表删除，创建新列表...（redis 服务器有影响，web 服务器没影响）
    lua_script = """
        local index = tonumber(ARGV[1])
        local list_key = KEYS[1]
        local len = redis.call("LLEN", list_key)

        if index < 0 then
            index = len + index  -- 处理负索引
        end

        if index >= len or index < 0 then
            return nil  -- 索引超出范围
        end

        redis.log(redis.LOG_NOTICE, "index: " .. index)

        local first_part, second_part
        if index == 0 then
            -- 如果 index 是 0，直接处理。因为 redis.call("LRANGE", list_key, 0, index - 1) 返回的不是空列表！
            first_part = {}
            second_part = redis.call("LRANGE", list_key, 1, -1)  -- 从 1 到 -1 获取后面的部分
        else
            first_part = redis.call("LRANGE", list_key, 0, index - 1)
            second_part = redis.call("LRANGE", list_key, index + 1, -1)
        end

        redis.call("DEL", list_key)  -- 删除原列表
        for _, v in ipairs(first_part) do
            redis.call("RPUSH", list_key, v)  -- 重新添加前面的部分
        end

        for _, v in ipairs(second_part) do
            redis.call("RPUSH", list_key, v)  -- 重新添加后面的部分
        end

        return 1  -- 返回成功
    """
    return db.eval(lua_script, 1, TODO_LIST_KEY, index)


# todo: 为了避免多进程 runserver 影响，直接操作 redis 来存放全局标记？
_loaded_data = False


def load_data():
    global _loaded_data
    if not _loaded_data:
        _loaded_data = True
        # todos: List[bytes] = db.lrange(TODO_LIST_KEY, 0, -1)
        # for todo in todos:
        #     db.rpush(TODO_LIST_KEY, todo)


@app.get(f"{BASE_URL}")
def list_todo():
    load_data()

    todos: List[bytes] = db.lrange(TODO_LIST_KEY, 0, -1)

    # 注意，返回的 todos 是 bytes 列表，需要转为 str 才能被 JSON 序列化
    return {"data": [re.sub(r"^.*\\|", "", e.decode("utf-8"), 1) for e in todos]}


@app.post(f"{BASE_URL}")
def create_todo(request: Request, value: str = Form(...)):
    index = db.rpush(TODO_LIST_KEY, value.encode("utf-8"))
    return {"data": {"index": index}}


@app.delete(f"{BASE_URL}" + "/delete")
def delete_todo(request: Request, index: int):
    if _remove_element_by_index(index) is None:
        raise HTTPException(400, {"message": f"delete todo task: {index} failed."})

    return {"message": f"delete todo task: {index} successfully."}


@app.post(f"{BASE_URL}" + "/{index}")
def update_todo(request: Request, index: int, content: str = Form(...)):
    _check_index(index)

    db.lset(TODO_LIST_KEY, index, content)
    return {"message": f"update todo task: {index} successfully."}


@app.get(f"{BASE_URL}" + "/{index}")
def get_todo(request: Request, index: int):
    load_data()

    _check_index(index)
    data = db.lrange(TODO_LIST_KEY, index, index)
    return {"data": data[0].decode("utf-8")}
