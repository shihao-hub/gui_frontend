1. "所有数据库映射类使用 Model/Entity 后缀，API 校验模型使用 Schema 后缀，跨服务传输对象使用 DTO 后缀"
2. 如果目录结构为：`utils/file_utils/__init__.py` 和 `utils/cache.py`，
   则 `__init__.py` 理当和 `base.py` 视为同级，`file_utils` 下的其他文件不是！
   规约之所以如此，是因为 `file_utils.py` -> `file_utils/__init__.py` 对于用户来说，应该是透明无感知的！ 