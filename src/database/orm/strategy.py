from enum import Enum

from beanie import PydanticObjectId
from pydantic import Field
from pymongo import IndexModel

from src.entity.strategy import VirtualAccount

from ._base import BaseDocument


class StrategyLevelEnum(str, Enum):
    """策略层级"""

    # 根节点
    ROOT = "ROOT"
    # 子节点
    CHILD = "CHILD"


class StrategyNode(BaseDocument):
    fund_id: int = Field(..., description="基金id")
    parent_id: PydanticObjectId | None = Field(default=None, description="父节点id, 根节点为None")
    weight: float = Field(default=1, description="权重, 0~1, 同一层级权重之和为1")
    name: str = Field(..., description="节点名称")
    info: dict | None = Field(default=None, description="策略信息")
    virtual_account: VirtualAccount = Field(default=VirtualAccount(), description="虚拟账户")

    class Settings:
        name = "strategy_node"
        indexes = [
            IndexModel("fund_id"),
        ]


class RootStrategyNode(StrategyNode):
    """根节点"""

    class Settings:
        name = "root_strategy_node"
        indexes = [
            IndexModel("fund_id"),
        ]


# 如何策略调整
# 只能相邻的两级节点调整
# 比如 找到所有根节点的子节点，策略类型是指增的
