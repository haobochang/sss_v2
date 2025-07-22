"""
数据库连接测试用例

展示如何在测试中mock配置和测试数据库连接
"""

from unittest.mock import MagicMock, patch

import pytest

from config.sys_config import SysConfig
from db.database import DatabaseManager, generate_mysql_url


def test_generate_mysql_url_with_mock_config():
    """测试使用mock配置生成MySQL URL"""

    # 测试配置
    test_config = {"mysql_url": "mysql+pymysql://test_user:test_pass@test_host:3306/test_db"}

    # 创建测试配置实例
    test_sys_config = SysConfig.create_for_testing(test_config)

    # Mock sys_config
    with patch("db.database.sys_config", test_sys_config):
        mysql_url = generate_mysql_url()
        assert mysql_url == "mysql+pymysql://test_user:test_pass@test_host:3306/test_db"


def test_database_manager_with_mock_config():
    """测试数据库管理器使用mock配置"""

    # 测试配置
    test_config = {"mysql_url": "mysql+pymysql://test_user:test_pass@test_host:3306/test_db"}

    # 创建测试配置实例
    test_sys_config = SysConfig.create_for_testing(test_config)

    # Mock sys_config
    with patch("db.database.sys_config", test_sys_config):
        db_manager = DatabaseManager()

        # 测试同步引擎创建
        engine = db_manager.get_engine()
        assert engine is not None
        assert str(engine.url) == "mysql+pymysql://test_user:test_pass@test_host:3306/test_db"

        # 测试异步引擎创建
        async_engine = db_manager.get_async_engine()
        assert async_engine is not None
        assert (
            str(async_engine.url) == "mysql+aiomysql://test_user:test_pass@test_host:3306/test_db"
        )


def test_database_session_with_mock_config():
    """测试数据库会话使用mock配置"""

    # 测试配置
    test_config = {"mysql_url": "mysql+pymysql://test_user:test_pass@test_host:3306/test_db"}

    # 创建测试配置实例
    test_sys_config = SysConfig.create_for_testing(test_config)

    # Mock sys_config和SQLAlchemy
    with (
        patch("db.database.sys_config", test_sys_config),
        patch("sqlalchemy.create_engine") as mock_create_engine,
        patch("sqlalchemy.ext.asyncio.create_async_engine") as mock_create_async_engine,
    ):
        # Mock引擎
        mock_engine = MagicMock()
        mock_async_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        mock_create_async_engine.return_value = mock_async_engine

        db_manager = DatabaseManager()

        # 测试会话工厂
        session_factory = db_manager.get_session_factory()
        assert session_factory is not None

        # 测试异步会话工厂
        async_session_factory = db_manager.get_async_session_factory()
        assert async_session_factory is not None


def test_database_operations_with_mock_session():
    """测试数据库操作使用mock会话"""

    # 测试配置
    test_config = {"mysql_url": "mysql+pymysql://test_user:test_pass@test_host:3306/test_db"}

    # 创建测试配置实例
    test_sys_config = SysConfig.create_for_testing(test_config)

    # Mock所有数据库相关组件
    with (
        patch("db.database.sys_config", test_sys_config),
        patch("sqlalchemy.create_engine") as mock_create_engine,
        patch("sqlalchemy.orm.sessionmaker") as mock_sessionmaker,
    ):
        # Mock引擎和会话
        mock_engine = MagicMock()
        mock_session = MagicMock()
        mock_session_factory = MagicMock()

        mock_create_engine.return_value = mock_engine
        mock_sessionmaker.return_value = mock_session_factory
        mock_session_factory.return_value = mock_session

        # 模拟查询结果
        mock_result = MagicMock()
        mock_result.all.return_value = [MagicMock(), MagicMock()]  # 2个结果
        mock_session.query.return_value.filter.return_value.limit.return_value.all.return_value = (
            mock_result.all()
        )

        db_manager = DatabaseManager()

        # 测试会话上下文管理器
        with db_manager.get_session() as session:
            # 模拟查询操作
            result = session.query(MagicMock()).filter().limit(10).all()
            assert len(result) == 2


def test_database_error_handling():
    """测试数据库错误处理"""

    # 测试配置
    test_config = {"mysql_url": "mysql+pymysql://test_user:test_pass@test_host:3306/test_db"}

    # 创建测试配置实例
    test_sys_config = SysConfig.create_for_testing(test_config)

    # Mock数据库组件
    with (
        patch("db.database.sys_config", test_sys_config),
        patch("sqlalchemy.create_engine") as mock_create_engine,
        patch("sqlalchemy.orm.sessionmaker") as mock_sessionmaker,
    ):
        # Mock引擎和会话
        mock_engine = MagicMock()
        mock_session = MagicMock()
        mock_session_factory = MagicMock()

        mock_create_engine.return_value = mock_engine
        mock_sessionmaker.return_value = mock_session_factory
        mock_session_factory.return_value = mock_session

        # 模拟数据库错误
        mock_session.query.side_effect = Exception("Database error")

        db_manager = DatabaseManager()

        # 测试错误处理
        with pytest.raises(Exception):
            with db_manager.get_session() as session:
                session.query(MagicMock()).all()

        # 验证回滚被调用
        mock_session.rollback.assert_called_once()


def test_config_validation():
    """测试配置验证"""

    # 测试空配置
    empty_config = {}
    test_sys_config = SysConfig.create_for_testing(empty_config)

    with patch("db.database.sys_config", test_sys_config):
        # 应该抛出错误，因为mysql_url为空
        with pytest.raises(ValueError, match="MySQL URL not configured"):
            generate_mysql_url()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
