__all__ = ["TodoListService"]

import abc
import uuid
from typing import List, Dict, TypedDict

from bson import ObjectId

from nicegui_start_project.utils.mvc import Service
from ..models import TodoListTypedDict, TodoList


class TodoListService(Service):

    def add_todo(self, task: str) -> None:
        this = self
        if task.strip():
            TodoList.objects.create(**{"task": task, "done": False})

    def get_todos(self) -> List[TodoListTypedDict]:
        this = self
        res = []
        for todo in TodoList.objects.all():
            todo: TodoList
            res.append(dict(uid=str(todo.id), task=todo.task, done=todo.done))
        return res

    def toggle_done(self, uid: str) -> None:
        this = self
        todolist: TodoList = TodoList.objects.get(id=ObjectId(uid))
        todolist.done = not todolist.done
        todolist.save()
