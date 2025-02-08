__all__ = ["AiApi", "refresh_question_answer"]

import json
import time
import traceback
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Dict, Tuple, Union, List
from multiprocessing import Process

import requests
from loguru import logger as log  # 当你发现某件事情比较麻烦的时候，可以去找一下第三方库

from projects.ag import configs


# immutable

# mutable


def refresh_question_answer(data: Dict) -> requests.Response:
    try:
        # note: try except 可以隔离作用域
        url = configs.CLIENT_BASE_URL + "/api/refresh_question_answer"
        response = requests.post(url, json=data)

        if response.status_code != 200:
            log.error(f"{response.status_code}, {response.text}")
        else:
            pass
        return response
    except Exception as e:
        log.error(f"{e}\n{traceback.format_exc()}")


class AiApi:

    def __init__(self, messages, ai_api_struct, settings):
        self.messages = messages

        self.ai_api_struct = ai_api_struct
        self.settings = settings

        self.thread_pool = ThreadPoolExecutor(max_workers=1)  # 线程池

    def _generate_prompt(self, raw_question: str):
        _ = self
        return raw_question

    def _persist_messages(self):
        _ = self
        filename = f"./ag2_{time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))}.json"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.messages, ensure_ascii=False))
        # log.info("Persisting messages success!")

    def _attempt_to_clear_messages(self):
        _ = self
        messages = self.messages

        if len(messages) >= self.settings.MESSAGES_MAX_SIZE:
            self._persist_messages()
            messages.clear()

    def _generate_request_data(self, message):
        _ = self
        return {
            "message": message,
            "mode": self.ai_api_struct.MODE,
            "prompt_id": self.ai_api_struct.PROMPTR_ID,
            "key": self.ai_api_struct.KEY
        }

    def _print_and_get_response_content(self, response, get=True, question="", enabled_print=True):
        content = []

        for line in response.iter_lines():
            if line is None:
                continue

            output = line.decode("utf-8")
            content.append(output)

            if self.settings.PRINT_IN_ONE_BREATH:
                continue

            if enabled_print:
                if self.settings.SIMULATE_TYPEWRITER_EFFECT:
                    for e in output:
                        time.sleep(0.02)
                        print(e, end="", flush=True)
                    print()
                else:
                    print(output)

        if get:
            res = "\n".join(content)

            if enabled_print:
                if self.settings.PRINT_IN_ONE_BREATH:
                    print(res, flush=True)

            # frontend
            future = self.thread_pool.submit(lambda: refresh_question_answer({"content": res}))

            return res

    def invoke_ai_api(self, question: str, enabled_print=True):
        self._attempt_to_clear_messages()

        prompt = self._generate_prompt(question)
        self.messages.append({
            "role": "user",
            "content": prompt
        })

        print(f"{self.ai_api_struct.MODE} 回复：", end="", flush=True)
        response = requests.post(self.ai_api_struct.URL,
                                 json=self._generate_request_data(self.messages),
                                 stream=True,
                                 verify=False)

        self.messages.append({
            "role": "assistant",
            "content": self._print_and_get_response_content(response, question=prompt, enabled_print=enabled_print)
        })
        print()

    def ask_english_ai(self, prompt: str):
        _ = self
        init_prompt = """
            在接下来的对话中，你要帮助我学习英语。因为我的英语水平有限，所以拼写可能会不准确，如果语句不通顺，请猜测我要表达的意思。在之后的对话中，除了正常理解并回复我的问题以外，还要指出我说的英文中的语法错误和拼写错误。
            并且在以后的对话中都要按照以下格式回复:
            【翻译】此处将英文翻译成中文
            【回复】此处写你的正常回复
            【勘误】此处写我说的英文中的语法错误和拼写错误，如果夹杂汉字，请告诉我它的英文
            【提示】如果有更好或更加礼貌的英文表达方式，在此处告诉我如果你能明白并能够照做
            请说“我明白了”
        """
        message = [
            {
                "role": "user",
                "content": init_prompt
            },
            {
                "role": "assistant",
                "content": "我明白了。"

            },
            {
                "role": "user",
                "content": prompt,
            }
        ]
        print(f"{self.ai_api_struct.MODE} 回复：", flush=True)
        response = requests.post(self.ai_api_struct.URL,
                                 json=self._generate_request_data(message),
                                 stream=True,
                                 verify=False)
        self._print_and_get_response_content(response, get=False, question=prompt)
