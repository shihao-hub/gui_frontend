"""
### 需求分析
- 序列化：运行的时候将 mongodb 数据库序列化为 json 文件
- 反序列化：清空 mongodb 数据库，使用 json 文件进行数据库初始化

"""

import argparse

from loguru import logger

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="负责将 mongodb 数据库的数据序列化和反序列化")
    parser.add_argument("action", type=str, choices=["serialize", "deserialize"],
                        help="操作类型，可选值必须为 serialize 或 deserialize")

    args = parser.parse_args()
    logger.info(args.action)
