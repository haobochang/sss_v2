"""
自定义异常和异常处理器
"""

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from .response import error_response


class ApiException(HTTPException):
    """API异常基类"""

    def __init__(self, msg: str, code: int = 1, status_code: int = 400):
        super().__init__(status_code=status_code, detail=msg)
        self.msg = msg
        self.code = code


async def api_exception_handler(request: Request, exc: Exception):
    """API异常处理器"""
    if isinstance(exc, ApiException):
        return JSONResponse(
            status_code=exc.status_code, content=error_response(exc.msg, exc.code).model_dump()
        )
    return JSONResponse(status_code=500, content=error_response(str(exc), 500).model_dump())


async def http_exception_handler(request: Request, exc: Exception):
    """HTTP异常处理器"""
    if isinstance(exc, StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(str(exc.detail), exc.status_code).model_dump(),
        )
    return JSONResponse(status_code=500, content=error_response(str(exc), 500).model_dump())
