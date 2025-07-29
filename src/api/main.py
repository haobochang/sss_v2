"""
FastAPI应用主入口
使用最佳实践进行应用初始化
"""

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .exceptions import (
    ApiException,
    api_exception_handler,
    http_exception_handler,
)
from .routers import example, fund


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    使用context manager模式管理启动和关闭事件
    """
    # 启动时执行
    from src.database.client import init_db  # noqa: PLC0415

    await init_db()
    yield

    # 关闭时执行
    # 可以在这里添加清理逻辑，如关闭数据库连接等


def create_app() -> FastAPI:
    """
    创建FastAPI应用实例
    使用工厂模式，便于测试和配置管理
    """
    app = FastAPI(
        title="SSS API",
        description="SSS系统API文档",
        version="1.0.0",
        lifespan=lifespan,
        root_path="/api/v1",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # 注册中间件
    setup_middleware(app)

    # 注册异常处理器
    setup_exception_handlers(app)

    # 注册路由
    setup_routers(app)

    return app


def setup_middleware(app: FastAPI) -> None:
    """配置中间件"""

    # CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 生产环境中应该指定具体的域名
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """配置异常处理器"""

    app.add_exception_handler(ApiException, api_exception_handler)
    app.add_exception_handler(Exception, http_exception_handler)


def setup_routers(app: FastAPI) -> None:
    """注册路由"""

    # 示例路由
    app.include_router(example.router, prefix="/examples", tags=["示例"])

    # 基金路由
    app.include_router(fund.router, prefix="/funds", tags=["基金"])


# 创建应用实例
app = create_app()


# 健康检查端点
@app.get("/health", tags=["系统"])
async def health_check() -> dict[str, Any]:
    """健康检查端点"""
    return {"status": "healthy", "message": "服务运行正常"}


# 根路径重定向到文档
@app.get("/", tags=["系统"])
async def root() -> dict[str, str]:
    """根路径，重定向到API文档"""
    return {"message": "欢迎使用SSS API", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
