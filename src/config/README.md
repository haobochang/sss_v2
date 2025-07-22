# 配置系统设计说明

## 概述

这个简化配置系统直接使用 SysConfig 类定义配置字段，提供类型提示、代码补全和动态刷新能力。

## 架构设计

### 核心组件

1. **SysConfig** 类
   - 直接定义配置字段使用 @property
   - 每个 property 从 dyn_config 动态获取值
   - 提供类型提示和文档字符串
   - 支持通用 get 方法和 get_all 方法

## 使用方法

### 基本使用

```python
from src.config.sys_config import sys_config

# 直接访问属性（有类型提示）
mysql_url = sys_config.mysql_url

# 对于未定义的键，使用 get 方法
redis_url = sys_config.get("redis_url", "default_value")
```

### 高级功能

```python
# 获取所有配置
all_config = sys_config.get_all()
```

## 添加新配置项

### 步骤：在 SysConfig 中添加 property

```python
class SysConfig:
    @property
    def mysql_url(self) -> str:
        """MySQL数据库连接URL"""
        return dyn_config.get('mysql_url', '')
    
    @property
    def redis_url(self) -> str:
        """Redis连接URL"""
        return dyn_config.get('redis_url', 'default_redis')  # 新增
    
    @property
    def api_key(self) -> str:
        """API密钥"""
        return dyn_config.get('api_key', '')  # 新增
    
    @property
    def debug(self) -> bool:
        """调试模式"""
        return dyn_config.get_bool('debug', False)  # 新增
```

### 使用新配置

```python
redis_url = sys_config.redis_url  # 有类型提示
api_key = sys_config.api_key
debug_mode = sys_config.debug
```

## 设计优势

1. **简单性**：直接在类中定义所有配置键
2. **类型安全**：属性有明确类型返回
3. **动态更新**：每次访问从 dyn_config 获取最新值
4. **开发体验**：IDE代码补全和提示
5. **可扩展性**：易于添加新 property

## 错误处理

- 如果键不存在，dyn_config.get() 返回默认值
- 对于未定义的属性访问，会抛出 AttributeError（推荐使用 get()）

## 最佳实践

1. **为每个配置键定义 property**：确保类型提示
2. **使用合适的默认值**：在 get() 中指定
3. **添加文档字符串**：描述每个配置的作用
4. **定期审查配置键**：保持定义的完整性 