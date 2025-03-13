import json
import pprint
import unittest
import uuid
from concurrent import futures
from collections import deque as safe_deque
from typing import List

import requests
from requests import HTTPError
from loguru import logger


class TestCase(unittest.TestCase):
    def setUp(self):
        with open("./resources/routes.json", "r") as f:
            self.routes: List[str] = json.load(f)

        self.thread_pool = futures.ThreadPoolExecutor(max_workers=4)

    def tearDown(self):
        pass

    def test_home_pages(self):
        shared_deque = safe_deque()

        def visit(url):
            try:
                response = requests.get(url, timeout=1)
                response.raise_for_status()
            except Exception as e:
                shared_deque.append(f"Error: {e}")

        future_list = [self.thread_pool.submit(visit, f"http://localhost:12000{route}") for route in self.routes]
        futures.wait(future_list)
        self.assertEqual(len(shared_deque), 0, f"Errors: \n{"\n".join(shared_deque)}")


if __name__ == '__main__':
    unittest.main()
