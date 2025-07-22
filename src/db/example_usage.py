"""
数据库连接使用示例

展示如何使用数据库连接管理模块进行同步和异步数据库操作
"""

import asyncio

from db.database import get_async_db_session, get_db_session, get_engine
from db.models import BlacklistConfig  # 假设这是你的模型


def example_sync_database_operations():
    """同步数据库操作示例"""

    # 方式1: 使用上下文管理器（推荐）
    with get_db_session() as session:
        # 查询数据
        blacklist_configs = session.query(BlacklistConfig).limit(10).all()
        print(f"Found {len(blacklist_configs)} blacklist configs")

        # 创建新记录
        new_config = BlacklistConfig(
            fund_code="TEST001", fund_name="Test Fund", broker_abbr="TEST", strategy="test_strategy"
        )
        session.add(new_config)
        # 提交会在上下文管理器退出时自动执行

    # 方式2: 直接使用引擎
    engine = get_engine()
    with engine.connect() as connection:
        result = connection.execute("SELECT COUNT(*) FROM blacklist_config")
        count = result.scalar()
        print(f"Total blacklist configs: {count}")


async def example_async_database_operations():
    """异步数据库操作示例"""

    async for session in get_async_db_session():
        # 查询数据
        from sqlalchemy import select

        stmt = select(BlacklistConfig).limit(10)
        result = await session.execute(stmt)
        blacklist_configs = result.scalars().all()
        print(f"Found {len(blacklist_configs)} blacklist configs (async)")

        # 创建新记录
        new_config = BlacklistConfig(
            fund_code="ASYNC001",
            fund_name="Async Test Fund",
            broker_abbr="ASYNC",
            strategy="async_strategy",
        )
        session.add(new_config)
        # 提交会在异步上下文管理器退出时自动执行


def example_bulk_operations():
    """批量操作示例"""

    with get_db_session() as session:
        # 批量插入
        configs_to_add = [
            BlacklistConfig(
                fund_code=f"BULK{i:03d}",
                fund_name=f"Bulk Fund {i}",
                broker_abbr="BULK",
                strategy="bulk_strategy",
            )
            for i in range(1, 6)
        ]

        session.add_all(configs_to_add)
        # 提交会在上下文管理器退出时自动执行
        print(f"Added {len(configs_to_add)} bulk configs")


async def example_async_bulk_operations():
    """异步批量操作示例"""

    async for session in get_async_db_session():
        # 批量插入
        configs_to_add = [
            BlacklistConfig(
                fund_code=f"ASYNC_BULK{i:03d}",
                fund_name=f"Async Bulk Fund {i}",
                broker_abbr="ASYNC_BULK",
                strategy="async_bulk_strategy",
            )
            for i in range(1, 6)
        ]

        session.add_all(configs_to_add)
        # 提交会在异步上下文管理器退出时自动执行
        print(f"Added {len(configs_to_add)} async bulk configs")


def example_error_handling():
    """错误处理示例"""

    try:
        with get_db_session() as session:
            # 尝试执行一个会失败的查询
            result = (
                session.query(BlacklistConfig)
                .filter(BlacklistConfig.fund_code == "NON_EXISTENT")
                .first()
            )

            # 模拟一个错误
            raise ValueError("Simulated error")

    except Exception as e:
        print(f"Caught error: {e}")
        # 事务会自动回滚


async def example_async_error_handling():
    """异步错误处理示例"""

    try:
        async for session in get_async_db_session():
            # 尝试执行一个会失败的查询
            from sqlalchemy import select

            stmt = select(BlacklistConfig).where(BlacklistConfig.fund_code == "NON_EXISTENT")
            result = await session.execute(stmt)

            # 模拟一个错误
            raise ValueError("Simulated async error")

    except Exception as e:
        print(f"Caught async error: {e}")
        # 事务会自动回滚


def run_examples():
    """运行所有示例"""
    print("=== 同步数据库操作示例 ===")
    example_sync_database_operations()

    print("\n=== 批量操作示例 ===")
    example_bulk_operations()

    print("\n=== 错误处理示例 ===")
    example_error_handling()

    print("\n=== 异步数据库操作示例 ===")
    asyncio.run(example_async_database_operations())

    print("\n=== 异步批量操作示例 ===")
    asyncio.run(example_async_bulk_operations())

    print("\n=== 异步错误处理示例 ===")
    asyncio.run(example_async_error_handling())


if __name__ == "__main__":
    run_examples()
