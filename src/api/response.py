"""
统一响应格式

成功响应格式：
{
    "code": 0,
    "msg": "success",
    "data": {...}
}

错误响应格式：
{
    "code": 1,
    "msg": "error message",
    "data": null
}
"""

from typing import Any, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse[T](BaseModel):
    """统一API响应模型"""

    code: int = Field(description="响应状态码，0表示成功，非0表示失败")
    msg: str = Field(description="响应消息")
    data: T = Field(..., description="响应数据")


def success_response(data: Any, msg: str = "success") -> ApiResponse:
    """成功响应"""
    return ApiResponse(code=0, msg=msg, data=data)


def error_response(msg: str, code: int = 1) -> ApiResponse:
    """错误响应"""
    return ApiResponse(code=code, msg=msg, data=None)
