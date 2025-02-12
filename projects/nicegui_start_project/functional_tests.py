"""
### 题外话
1. 今日计算 deepseek 访问量时想到了 django 那本书里关于网站访问量的计算。
   突然意识到，其实大部分人都需要大量刷题，灵感骤现除了那天生的天赋，还有就是大量知识的支撑。
   对于普通人而言，显然后者才是唯一的选择。
   当然，访问量的计算是因为简单，当时就记住了，所以今天才能迅速联想到。
   但是这终究还是体现了知识的广度和深度的重要性。
   因此不必泄气，好身体 + 持续学习，剩下的就交给时间吧。

"""

import unittest

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.HOMEPAGE = "http://localhost:8900"

        # driver = webdriver.Firefox(service=webdriver.FirefoxService(GeckoDriverManager().install()))

        self.browser = webdriver.Firefox(service=webdriver.FirefoxService("./bin/geckodriver.exe"))

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 用户访问某个在线待办事项应用的首页
        self.browser.get(self.HOMEPAGE)

        # 用户注意到网页的标题和头部都包含 To-Do 这个词
        self.assertIn("To-Do", self.browser.title)
        self.fail("Finish the test!")

        # 应用邀请用户输入一个待办事项

        # 用户在文本框输入 Buy peacock feathers（购买孔雀羽毛）
        # 用户按下回车键后，页面更新了
        # 待办事项表格中显示了 “1: Buy peacock feathers”


if __name__ == '__main__':
    unittest.main(warnings="ignore")
