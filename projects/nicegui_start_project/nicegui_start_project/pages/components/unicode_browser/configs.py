from pathlib import Path

PAGE_ICON = "✍️"
PAGE_TITLE = "Unicode 字符浏览器"
PAGE_PATH = "/pages/components/unicode_browser"
VERSION = "1.0.0"

COMPONENT_SOURCE_DIR = Path(__file__).resolve().parent

# 预定义的 Unicode 类别范围（示例）
UNICODE_CATEGORIES = {
    "表情符号": [
        (0x1F600, 0x1F64F),  # 表情符号
        (0x1F680, 0x1F6FF),  # 交通和地图符号
    ],
    "货币符号": [
        (0x20A0, 0x20CF),  # 货币符号
    ],
    "箭头": [
        (0x2190, 0x21FF),  # 箭头
    ],
    "数学符号": [
        (0x2200, 0x22FF),  # 数学运算符
    ],
    "中文符号": [
        (0x3000, 0x303F),  # 中文标点
    ],
    "字母": [
        (0x0041, 0x005A),  # 大写字母
        (0x0061, 0x007A),  # 小写字母
    ]
}
