"""
### 编码建议
1. 建议参考 django 的 manager.py 的实现，目前简单的认知是复杂的 OOP

### 需求分析
1. 启动项目命令：python manager.py startup
2. 创建模板命令：python manager.py create_component_template --name xx --filename xx

"""
import abc
import argparse
import shutil
import sys
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import TypedDict

from loguru import logger
from pydantic import BaseModel

PYTHON_EXE: str = sys.executable
BASE_DIR: Path = Path(__file__).parent.parent
SOURCE_DIR: Path = Path(__file__).parent

TEMPLATES = {
    "__init__.py": """
""",
    "configs.py": """\
PAGE_ICON = "✍️"
PAGE_TITLE = "{page_title}"
PAGE_PATH = "{page_path}"
VERSION = ""
""",
    "pages.py": """\
from nicegui import ui

from . import configs


@ui.page(configs.PAGE_PATH, title=configs.PAGE_TITLE)
async def {main_page_function_name}():
    pass
"""
}


class TemplateInputData(abc.ABC):
    pass


@dataclass
class EmptyTemplateInputData(TemplateInputData):
    pass


@dataclass
class ConfigsTemplateInputData(TemplateInputData):
    page_title: str
    page_path: str


@dataclass
class PagesTemplateInputData(TemplateInputData):
    main_page_function_name: str


# class ConfigsInputDataSchema(BaseModel):
#     page_title: str
#     page_path: str
#
#
# class PagesInputDataSchema(BaseModel):
#     main_page_function_name: str


def handle_startup():
    """处理启动项目的逻辑"""
    # "{PYTHON_EXE}" 会提示：文件名、目录名或卷标语法不正确。为什么呢？那假如目录有空格，岂不是会有问题？
    assert " " not in PYTHON_EXE
    os.system(f'{PYTHON_EXE} "{SOURCE_DIR}/main.py"')


def _create_component_template_file(name: str, filename: str):
    """创建组件模板文件"""
    logger.info(f"🛠️ Creating component template file: {name} -> {filename}")
    template = TEMPLATES.get(filename)
    assert template is not None

    component_dir = SOURCE_DIR / "pages" / "components" / name
    filepath = component_dir / filename

    if not component_dir.exists():
        logger.error(f"组件 {name} 不存在")
        return

    if filepath.exists():
        logger.error(f"文件 {filename} 已存在")
        return

    input_data = EmptyTemplateInputData()
    if filename == "configs.py":
        input_data = ConfigsTemplateInputData(
            page_title=name.upper(),
            page_path=f"/pages/components/{name}"
        )
    elif filename == "pages.py":
        input_data = PagesTemplateInputData(
            main_page_function_name=f"{name}"
        )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(template.format(**asdict(input_data)))


def handle_create_component_template_dir(name: str):
    # subflow A
    # 判断组件是否存在
    #   如果存在则退出
    # 如果组件不存在，则创建所有模板文件

    # subflow B
    # 如果创建失败，则删除所有文件

    def rollback():
        shutil.rmtree(f"{component_dir}")
        logger.info("🔙 创建组件模板失败，进行回滚操作")

    component_dir = SOURCE_DIR / "pages" / "components" / name
    if component_dir.exists():
        logger.error(f"组件 {name} 已存在")
        return

    try:
        component_dir.mkdir(parents=True)
        for filename in TEMPLATES.keys():
            _create_component_template_file(name, filename)
    except Exception as e:
        logger.error(f"创建组件模板失败，原因：{e}")
        rollback()


def main():
    # 主解析器
    parser = argparse.ArgumentParser(description="项目管理实用程序")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 添加 startup 子命令
    startup_parser = subparsers.add_parser("startup", help="启动项目")

    # 添加 create_component_template_dir 子命令及参数
    create_parser = subparsers.add_parser("create_component_template_dir", help="创建组件模板")
    create_parser.add_argument("--name", type=str, required=True, help="组件名")

    # 添加 create_component_template_file 子命令及参数
    # create_parser = subparsers.add_parser("create_component_template_file", help="创建组件模板文件")
    # create_parser.add_argument("--name", type=str, required=True, help="组件名")
    # create_parser.add_argument("--filename", type=str, required=True,
    #                            choices=list(TEMPLATES.keys()), help="指定创建的文件名")

    # 解析参数
    args = parser.parse_args()

    # 根据命令分发逻辑
    if args.command == "startup":
        handle_startup()
    elif args.command == "create_component_template_dir":
        handle_create_component_template_dir(args.name)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
