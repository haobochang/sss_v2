from re import S

from config_center import Config

CONFIG_CENTER_APP = "app.sss_v2"


class SysConfig:
    """系统配置类，直接使用config_center初始化动态配置

    使用Pydantic模型声明配置键，避免重复样板代码
    """

    def __init__(self, override_files: list[str] | None = None):
        """
        初始化配置

        Args:
            override_files: 用于测试的配置文件列表，优先级从低到高
        """
        self._dyn_config = Config(app=CONFIG_CENTER_APP, override=override_files or [])

    #########################################################
    # 以下是动态属性，用于提供更好的IDE代码提示和类型检查
    # 每次访问时都会从dyn_config动态获取最新值
    #########################################################
    @property
    def mysql_url(self) -> str:
        """MySQL数据库连接URL"""
        return self._dyn_config.get("mysql_url", "")


# 创建全局配置单例
sys_config = SysConfig()

print(sys_config._dyn_config.items())
