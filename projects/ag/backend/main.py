from concurrent import futures
from typing import Callable, TypedDict, Optional

import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, Query
from fastapi.requests import Request

from projects.ag import configs
from projects.ag.backend.tools.ag import ai_api
from projects.ag.backend.ai import refresh_question_answer

app = FastAPI()

just_one_thread_pool = futures.ThreadPoolExecutor(max_workers=1)


def bat_setup():
    import sys
    from pathlib import Path

    # 获取当前文件的绝对路径，然后定位到 gui_frontend 目录
    current_dir = Path(__file__).resolve().parent
    frontend_dir = current_dir.parent.parent.parent  # 根据层级调整
    sys.path.append(str(frontend_dir))


bat_setup()


class InvokeAiApiRequest(BaseModel):
    question: str


@app.post("/api/invoke_ai_api")
def invoke_ai_api(request: Request, body: InvokeAiApiRequest):
    try:
        question = body.question
        if not question.strip():
            return 400, {"message": "please input valid question"}

        just_one_thread_pool.submit(lambda: refresh_question_answer({"question": question}))
        just_one_thread_pool.submit(lambda: ai_api.invoke_ai_api(question, enabled_print=True))
        return 200, {"message": "success"}
    except Exception as e:
        return 500, {"message": f"Error: {e}"}


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=configs.SERVER_PORT, reload=False)
