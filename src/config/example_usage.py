"""
配置系统使用示例

这个文件展示了如何使用新的简化配置系统。
"""

from .sys_config import sys_config


def example_basic_usage():
    """基本使用示例"""

    # 直接使用 sys_config 的属性（有类型提示和代码补全）
    mysql_url = sys_config.mysql_url
    print(f"MySQL URL: {mysql_url}")

    # 对于未定义的配置，使用 get 方法
    redis_url = sys_config.get("redis_url", "default_redis_url")
    print(f"Redis URL: {redis_url}")


def example_advanced_usage():
    """高级使用示例"""

    # 获取所有配置
    all_config = sys_config.get_all()
    print(f"All config: {all_config}")


def example_adding_new_config():
    """添加新配置项的示例"""

    # 在 SysConfig 类中添加新的 property
    # @property
    # def redis_url(self) -> str:
    #     """Redis连接URL"""
    #     return dyn_config.get('redis_url', 'default_redis')
    #
    # @property
    # def api_key(self) -> str:
    #     """API密钥"""
    #     return dyn_config.get('api_key', '')
    #
    # @property
    # def debug(self) -> bool:
    #     """调试模式"""
    #     return dyn_config.get_bool('debug', False)

    # 然后就可以使用
    # redis_url = sys_config.redis_url  # 现在有类型提示


if __name__ == "__main__":
    print("=== 基本使用示例 ===")
    example_basic_usage()

    print("\n=== 高级使用示例 ===")
    example_advanced_usage()

    print("\n=== 添加新配置示例 ===")
    example_adding_new_config()
