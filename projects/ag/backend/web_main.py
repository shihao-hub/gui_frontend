__all__ = ["get_run"]

from concurrent import futures
from typing import Callable, TypedDict, Optional

from flask import Flask, request

app = Flask(__name__)


class Context(TypedDict):
    invoke_ai_api: Callable


# 能这样用吗？这是类型提示，不能实例化的吧
context: Optional[Context] = None

just_one_thread_pool = futures.ThreadPoolExecutor(max_workers=1)


@app.route("/hello", methods=['GET'])
def hello():
    question = request.args.get("question", "default question")
    # 去空
    if not question.strip():
        return "Success"

    print(context)
    l_context = context or {}
    invoke_ai_api = l_context.get("invoke_ai_api")
    print(f"messages: {len(messages)}")
    if invoke_ai_api:
        just_one_thread_pool.submit(lambda: invoke_ai_api(question))  # 我的上一个问题是什么
        return "Success"
    return "Error"


def run():
    app.run(host="localhost", port=9001)


def get_run(invoke_ai_api: Callable):
    global context
    context = {
        "invoke_ai_api": invoke_ai_api
    }
    print(context)

    return run


if __name__ == '__main__':
    def init():
        from main import invoke_ai_api

        global context

        assert context is None
        context = {
            "invoke_ai_api": invoke_ai_api
        }


    from main import messages

    init()

    run()
