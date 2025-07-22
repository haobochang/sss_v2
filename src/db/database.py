"""
数据库连接管理模块

提供数据库引擎创建、会话管理和连接池配置功能
"""

import logging
from collections.abc import AsyncGenerator, Generator
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool

from src.config import sys_config

logger = logging.getLogger(__name__)


def generate_mysql_url() -> str:
    """根据配置生成MySQL连接URL"""
    try:
        # 从配置中获取数据库连接信息
        mysql_url = sys_config.mysql_url

        if not mysql_url:
            # 如果配置中没有直接的mysql_url，尝试从其他配置构建
            # 这里可以根据实际配置结构调整
            raise ValueError("MySQL URL not configured")

        return mysql_url

    except Exception as e:
        logger.error(f"Failed to generate MySQL URL: {e}")
        raise


class DatabaseManager:
    """数据库管理器，负责引擎创建和会话管理"""

    def __init__(self):
        self._engine: Engine | None = None
        self._async_engine: AsyncEngine | None = None
        self._session_factory = None
        self._async_session_factory = None

    def get_engine(self) -> Engine:
        """获取同步数据库引擎"""
        if self._engine is None:
            self._engine = self._create_engine()
        return self._engine

    def get_async_engine(self) -> AsyncEngine:
        """获取异步数据库引擎"""
        if self._async_engine is None:
            self._async_engine = self._create_async_engine()
        return self._async_engine

    def _create_engine(self) -> Engine:
        """创建同步数据库引擎"""
        mysql_url = generate_mysql_url()

        engine = create_engine(
            mysql_url,
            poolclass=QueuePool,
            pool_size=10,  # 连接池大小
            max_overflow=20,  # 最大溢出连接数
            pool_pre_ping=True,  # 连接前ping检查
            pool_recycle=3600,  # 连接回收时间（秒）
            echo=False,  # 是否打印SQL语句
        )
        print(engine)
        logger.info("Synchronous database engine created successfully")
        return engine

    def _create_async_engine(self) -> AsyncEngine:
        """创建异步数据库引擎"""
        mysql_url = generate_mysql_url()

        # 转换为异步URL
        if mysql_url.startswith("mysql+pymysql://"):
            async_url = mysql_url.replace("mysql+pymysql://", "mysql+aiomysql://")
        else:
            async_url = mysql_url

        engine = create_async_engine(
            async_url,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False,
        )

        logger.info("Asynchronous database engine created successfully")
        return engine

    def get_session_factory(self):
        """获取会话工厂"""
        if self._session_factory is None:
            engine = self.get_engine()
            self._session_factory = sessionmaker(
                bind=engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
            )
        return self._session_factory

    def get_async_session_factory(self):
        """获取异步会话工厂"""
        if self._async_session_factory is None:
            engine = self.get_async_engine()
            self._async_session_factory = async_sessionmaker(
                bind=engine,
                class_=AsyncSession,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
            )
        return self._async_session_factory

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """获取数据库会话的上下文管理器"""
        session_factory = self.get_session_factory()
        session = session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """获取异步数据库会话"""
        session_factory = self.get_async_session_factory()
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    def dispose(self):
        """释放所有数据库连接"""
        if self._engine:
            self._engine.dispose()
            self._engine = None
        if self._async_engine:
            # 异步引擎的dispose需要等待
            import asyncio

            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # 如果事件循环正在运行，创建任务
                    loop.create_task(self._async_engine.dispose())
                else:
                    loop.run_until_complete(self._async_engine.dispose())
            except RuntimeError:
                # 如果没有事件循环，创建新的
                asyncio.run(self._async_engine.dispose())
            self._async_engine = None

        self._session_factory = None
        self._async_session_factory = None
        logger.info("Database connections disposed")


# 创建全局数据库管理器实例
db_manager = DatabaseManager()


# 便捷函数
def get_engine() -> Engine:
    """获取数据库引擎"""
    return db_manager.get_engine()


def get_async_engine() -> AsyncEngine:
    """获取异步数据库引擎"""
    return db_manager.get_async_engine()


def get_session_factory():
    """获取会话工厂"""
    return db_manager.get_session_factory()


def get_async_session_factory():
    """获取异步会话工厂"""
    return db_manager.get_async_session_factory()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """获取数据库会话的便捷函数"""
    with db_manager.get_session() as session:
        yield session


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """获取异步数据库会话的便捷函数"""
    async for session in db_manager.get_async_session():
        yield session
