# 数据库连接管理系统

## 概述

这个数据库连接管理系统提供了完整的数据库引擎创建、会话管理和连接池配置功能，支持同步和异步操作。

## 核心组件

### 1. DatabaseManager
- 负责数据库引擎的创建和管理
- 提供连接池配置
- 管理会话工厂
- 支持同步和异步操作

### 2. 配置集成
- 与 `config_center` 集成
- 支持测试时的配置mock
- 动态获取数据库连接信息

## 使用方法

### 基本使用

```python
from db.database import get_db_session, get_async_db_session

# 同步数据库操作
with get_db_session() as session:
    # 执行数据库操作
    result = session.query(YourModel).all()
    # 事务会自动提交

# 异步数据库操作
async for session in get_async_db_session():
    # 执行异步数据库操作
    stmt = select(YourModel)
    result = await session.execute(stmt)
    # 事务会自动提交
```

### 直接使用引擎

```python
from db.database import get_engine, get_async_engine

# 同步引擎
engine = get_engine()
with engine.connect() as connection:
    result = connection.execute("SELECT * FROM your_table")

# 异步引擎
async_engine = get_async_engine()
async with async_engine.connect() as connection:
    result = await connection.execute("SELECT * FROM your_table")
```

### 批量操作

```python
from db.database import get_db_session

with get_db_session() as session:
    # 批量插入
    objects_to_add = [YourModel(...) for _ in range(100)]
    session.add_all(objects_to_add)
    # 自动提交
```

## 配置要求

### 配置项

在 `config_center` 中需要配置：

```yaml
mysql_url: "mysql+pymysql://username:password@host:port/database"
```

### 配置示例

```python
# 根据你的配置生成MySQL URL
mysql_url = "mysql+pymysql://sss_test:0i8XnrzNc2i_w7B0@mysqltest03.dev.sci-inv.cn/sss_test"
```

## 连接池配置

默认连接池配置：
- `pool_size`: 10 (连接池大小)
- `max_overflow`: 20 (最大溢出连接数)
- `pool_pre_ping`: True (连接前ping检查)
- `pool_recycle`: 3600 (连接回收时间，秒)

## 错误处理

系统提供自动错误处理：
- 异常时自动回滚事务
- 自动关闭数据库连接
- 详细的错误日志记录

```python
try:
    with get_db_session() as session:
        # 数据库操作
        pass
except Exception as e:
    # 事务已自动回滚
    logger.error(f"Database operation failed: {e}")
```

## 测试支持

### Mock配置

```python
from config.sys_config import SysConfig
from unittest.mock import patch

# 创建测试配置
test_config = {
    'mysql_url': 'mysql+pymysql://test_user:test_pass@test_host:3306/test_db'
}
test_sys_config = SysConfig.create_for_testing(test_config)

# Mock配置
with patch('db.database.sys_config', test_sys_config):
    # 你的测试代码
    pass
```

### 测试示例

```python
def test_database_operations():
    # 测试配置
    test_config = {
        'mysql_url': 'mysql+pymysql://test_user:test_pass@test_host:3306/test_db'
    }
    test_sys_config = SysConfig.create_for_testing(test_config)
    
    # Mock配置和数据库组件
    with patch('db.database.sys_config', test_sys_config), \
         patch('sqlalchemy.create_engine') as mock_create_engine:
        
        # 测试数据库操作
        db_manager = DatabaseManager()
        engine = db_manager.get_engine()
        assert engine is not None
```

## 性能优化

### 1. 连接池优化
- 根据应用负载调整 `pool_size`
- 监控连接池使用情况
- 设置合适的 `pool_recycle` 时间

### 2. 异步操作
- 对于I/O密集型操作，使用异步数据库操作
- 避免在异步上下文中使用同步操作

### 3. 会话管理
- 及时释放数据库会话
- 使用上下文管理器确保资源清理
- 避免长时间持有会话

## 最佳实践

1. **使用上下文管理器**：确保事务正确提交和回滚
2. **错误处理**：捕获并处理数据库异常
3. **连接池监控**：定期检查连接池状态
4. **测试覆盖**：为数据库操作编写完整的测试
5. **配置管理**：使用配置中心管理数据库连接信息

## 依赖项

- SQLAlchemy 2.0+
- PyMySQL (同步)
- aiomysql (异步)
- config-center (配置管理)

## 故障排除

### 常见问题

1. **连接超时**：检查网络连接和数据库服务状态
2. **连接池耗尽**：增加 `pool_size` 或 `max_overflow`
3. **配置错误**：验证 `mysql_url` 格式和权限
4. **异步引擎错误**：确保安装了 `aiomysql` 包 