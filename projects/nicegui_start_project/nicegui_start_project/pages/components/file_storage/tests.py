import unittest


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_main(self):
        print(123)  # 为什么 pycharm 没有提示波浪线（未使用 self）


if __name__ == '__main__':
    unittest.main()
