import pprint
import re
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError, validate_call


class UserSchema(BaseModel):
    """
    密码强度检查：
    - 8 个字符以上
    - 必须包含数字
    - 必须包含大写字母
    - 必须包含特殊字符

    Usage:
        payload = {"name": "Bob", "email": "invalid", "password": "123"}
        try:
            UserCreateSchema(**payload)  # 触发校验异常
        except ValidationError as e:
            print(e)
    """
    name: str
    email: EmailStr
    password: str

    @field_validator("password")  # NOQA
    @classmethod
    def validate_password(cls, value):
        """密码强度验证器"""
        errors = []  # note: new ArrayList<TemplateError>() -> deepseek 妙哉，遇事不决，整理完需求立刻问一下 deepseek

        # 长度检查
        if len(value) < 8:
            errors.append("密码必须至少8个字符")

        # 数字检查
        if not re.search(r'\d', value):
            errors.append("密码必须包含至少1个数字")

        # 大写字母检查
        if not re.search(r'[A-Z]', value):
            errors.append("密码必须包含至少1个大写字母")

        # 特殊字符检查
        if not re.search(r'[@$!%*?&]', value):
            errors.append("密码必须包含至少1个特殊字符 (@$!%*?&)")

        if errors:
            raise ValueError("\n".join(errors))

        return value


if __name__ == '__main__':
    @validate_call
    def calculate_discount(price: float, discount: Annotated[float, Field(ge=0, le=1)]) -> float:
        return price * (1 - discount)


    calculate_discount(100, 0.2)  # 正常调用
    # calculate_discount(100, 1.5)  # 触发 ValidationError

    try:
        UserSchema(name="Bob", email="invalid", password="123")
    except ValidationError as e:
        pprint.pprint(e.errors())
