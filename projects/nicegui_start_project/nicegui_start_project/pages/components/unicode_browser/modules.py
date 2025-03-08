import dataclasses
import functools
import hashlib
import os
import traceback
import uuid
import time
from typing import List, Tuple

import requests
from loguru import logger

from nicegui import ui

from nicegui_start_project.utils import thread_pool, SingletonMeta
from .mediator import io_operation, thread_exception_handler


class RefreshNameLabelModule(metaclass=SingletonMeta):
    @dataclasses.dataclass
    class _NameLabel:
        label: ui.label
        content: str

    def __init__(self):
        # 提前保存元素引用（推荐）
        self._character_cards: List[ui.card] = []
        self._name_labels: List[RefreshNameLabelModule._NameLabel] = []

    @io_operation
    def youdao_translate(self, text: str) -> str:
        """有道翻译接口调用"""

        def _get_translation_result():
            def _calculate_sign() -> str:
                # sha256(应用ID/APP_KEY + input + salt + curtime + 应用密钥)
                ipt_len = len(text)
                ipt = text if ipt_len <= 20 else text[0:10] + str(ipt_len) + text[ipt_len - 10:ipt_len]

                str_src = app_key + ipt + salt + curtime + app_secret

                hash_algorithm = hashlib.sha256()
                hash_algorithm.update(str_src.encode('utf-8'))
                return hash_algorithm.hexdigest()

            url = "https://openapi.youdao.com/api"
            app_key = os.getenv("YOUDAO_APP_KEY", default="not-set")
            app_secret = os.getenv("YOUDAO_APP_SECRET", default="not-set")
            salt = str(uuid.uuid4())
            curtime = str(time.time())
            response = requests.post(url, json={
                "q": text,
                "from": "auto",
                "to": "zh-CHS",
                "appKey": app_key,
                "salt": salt,
                "sign": _calculate_sign(),
                "signType": "v3",
                "curtime": curtime,
            })
            data = response.json()

        try:
            # todo: 让这个能够成功调用
            raise NotImplementedError()
            # return "youdao_" + text
        except NotImplementedError:
            pass
        except Exception as e:
            logger.error(f"{e}\n{traceback.format_exc()}")
        return text

    def register_name_labels(self, name_label: ui.label, content: str):
        self._name_labels.append(self._NameLabel(name_label, content))

    def delay_refresh_name_labels(self):
        @thread_exception_handler
        def _update_name_labels():
            for elem in self._name_labels:
                res = self.youdao_translate(elem.content)
                if res == elem.content:
                    continue
                elem.label.text = self.youdao_translate(elem.content)
                elem.label.update()

        # todo: 注册到 body 加载完成后的回调中
        thread_pool.submit(lambda: _update_name_labels())
