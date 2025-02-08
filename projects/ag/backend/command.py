__all__ = ["get_process_command"]

import os
import re
import sys
import time
from abc import ABC, abstractmethod
from typing import TypedDict, List, Optional, Union, Tuple, Dict


class Context(TypedDict):
    KEY_WORDS: Union[List, Tuple]

    messages: List


g_context: Optional[Context] = None


class Command(ABC):

    @abstractmethod
    def execute(self, params: Union[Tuple, List] = None, named_params: Dict = None):
        pass


class SaveCommand(Command):
    """
        保存某次回答，-1 表示上一次，-2 表示倒数第二次，以此类推
        > 注意，index 支持正数和负数

        Usage:
        @cmd save [index] [name]
    """

    @staticmethod
    def create_directory(self, dir_path: str):
        raise NotImplemented

    # ------------------------------------------------------------------------------------------------------------ #
    @staticmethod
    def __handle_base_filename(base_filename: str):
        base_filename_no_suffix, file_suffix = os.path.splitext(base_filename)
        if not file_suffix:
            file_suffix = ".md"

        # 去掉所有特殊字符
        base_filename_no_suffix = re.sub(r"[\\/:*?\"<>|\s]", "", base_filename_no_suffix)

        # 最大长度为 255 个字符
        res = base_filename_no_suffix + file_suffix
        return res[:255]

    @staticmethod
    def write_file(content: str, base_filename: str = None):

        use_makedirs_function = False

        if base_filename is None:
            base_filename = f"{time.strftime('%Y-%m-%d-%H%M%S')}.md"
        else:
            # Notice, when we use the staticmethod of SaveCommand,
            # we need to consider the consequences when we alter the name of the SaveCommand class.
            base_filename = SaveCommand.__handle_base_filename(base_filename)

        dirs = ["resources", "ag2"]
        dir_path = "./" + "/".join(dirs) + "/"

        if use_makedirs_function:
            os.makedirs(dir_path, exist_ok=True)
        else:
            tmp_dir_path = "../../"
            for dirname in dirs:
                tmp_dir_path = tmp_dir_path + dirname + "/"
                if not os.path.exists(tmp_dir_path):
                    os.mkdir(tmp_dir_path)

        filename = os.path.join(dir_path, base_filename)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
            f.flush()

    def execute(self, params: Union[Tuple, List] = None, named_params: Dict = None):
        # params = params if params else None
        saved_file_basename = None

        # params would be None, [], or (), so we need use it with `if not params`.
        if not params:
            index = -1
        else:
            # Question:
            #   Whether I need to check the type of params?
            #   If someone uses the command such as `@cmd save abc`, this would cause a crash.
            index = int(params[0])

            # 1,1-1 | 2,3-1 | 3,5-1 | 4,7-1 | 5,9-1 ... ==> n,2*n-1-1
            # -1,-1 | -2,-3 | -3,-5 | -4,-7 | -5,-9 ... ==> n,2*n+1

            index = (2 * index + 1) if index < 0 else (2 * index - 1)

            # print("Test:", "{old_index}, {index}".format(old_index=params[0], index=index))

            if len(params) == 2:
                saved_file_basename = params[1]

        messages = g_context.get("messages")
        try:
            assert len(messages) % 2 == 0, "The length of `messages` field must be even."
            answer = messages[index].get("content")
            question = messages[index - 1].get("content")
            question = "\n".join(["> " + e + "  " for e in question.split("\n")])
            # 6*\n
            # <==>
            # > title \n -> because the `"\n".join` function does not append a newline after the last element.
            # \n -> `>` need have a newline with other element.
            # \n
            # \n -> markdown newline
            # \n
            # \n -> markdown newline
            self.write_file(f"{question}\n\n\n\n\n\n{answer}", base_filename=saved_file_basename)
            print("Saved file success!")
        except IndexError:
            print(f"Index overflow, excepted [0, {len(messages)}) or ({-(len(messages))}, -1]")

    # ------------------------------------------------------------------------------------------------------------ #


class SaveAllCommand(Command):

    def execute(self, params: Union[Tuple, List] = None, named_params: Dict = None):
        res = []

        messages = g_context.get("messages")
        assert len(messages) % 2 == 0, "The length of `messages` field must be even."
        i = 0
        while i < len(messages):
            raw_question = messages[i].get("content")
            question = "\n".join(["> " + e + "  " for e in raw_question.split("\n")])
            answer = messages[i + 1].get("content")
            res.append(f"{question}\n\n\n\n{answer}\n\n\n")
            i += 2

        SaveCommand.write_file("\n".join(res))
        print("Saved all files success!")


class HelpCommand(Command):
    # NOTE: 2025-01-11
    #   实战使用 Command, HelpCommand, SaveCommand 似乎体会到了开闭原则的力量，只需要创建新类即可！
    #   虽然我的逻辑中还得修改函数内容，但是实际上可以变成配置文件，然后通过配置文件来动态加载命令，从而真正实现开闭原则。
    def execute(self, params: Union[Tuple, List] = None, named_params: Dict = None):
        if not params:
            print("Usage:\n"
                  "    @cmd help list_keywords")
            return

        if params[0] == "list_keywords":
            print(f"Keywords:\n{"\n".join(g_context.get("KEYWORDS"))}")


# NOTE: 此处有一些影子：通过配置动态注入命令，只需要创建新类，并修改这个配置即可，不必修改 process_command 函数的逻辑！
COMMAND_MAP = {
    "save": SaveCommand,
    "saveall": SaveAllCommand,
    "help": HelpCommand,
}


def get_process_command(context: Context):
    # 依赖注入
    global g_context
    g_context = context

    def process_command(command: str):
        # The Command is split by the blank character. Such as: lua.exe sum.lua 1 2 3 4 5 <==> sum(...) -> 15
        words = command.strip().split(" ")

        # convert `words` into parameters and named parameters.
        params = []
        named_params = {}

        # NOTE: 此处的实现不知道是否合理，但是我有一点可以明确，那就是测试的重要性，只要软件质量得以满足，那就是好代码！
        #   软件质量：可靠性、可维护性、可移植性等
        i = 1
        while i < len(words):
            word = words[i]
            if word.startswith("--"):
                try:
                    named_params[word[2:]] = words[i + 1]
                except IndexError:
                    print(f"Invalid command: `{command}`")
                    return
                i += 1
            else:
                params.append(word)
            i += 1
        # `@cmd save -1 name --filename name --index -1` -> `['-1', 'f'] {'filename': 'name', 'index': '-1'}`
        # print(params, named_params)

        cls = COMMAND_MAP.get(words[0])
        if cls is None:
            print(f"Unknown command: {command}, expected: {(', '.join(COMMAND_MAP.keys()))}")
            return
        command_obj = cls()
        command_obj.execute(params, named_params)

    return process_command
