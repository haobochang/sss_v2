"""初始化数据"""

import asyncio

from rich import print as rprint

from src.database.orm import Fund, StrategyNode, StrategyTree, register_orm_models
from src.entity.strategy import VirtualAccount


async def init_data():
    """初始化数据"""
    await register_orm_models()
    # 创建一个基金
    await Fund.find_all().delete()
    await StrategyNode.find_all().delete()
    fund_75 = Fund(fund_id=75, name="旭日五", code="SR7446")
    await fund_75.insert()
    rprint(fund_75)

    # 给这个基金配置一个策略树
    root_node = StrategyNode(
        fund_id=75,
        parent_id=None,
        weight=1,
        name="root",
        info=None,
        virtual_account=VirtualAccount(),
    )
    await root_node.insert()

    rprint(root_node)

    # 给根节点配置两类策略，一个中性策略，一个指数增强策略

    # 中性策略
    neutral_strategy = StrategyNode(
        fund_id=75,
        parent_id=root_node.id,
        weight=0.5,
        name="中性策略",
        info=None,
        virtual_account=VirtualAccount(),
    )
    await neutral_strategy.insert()

    # 指数增强策略
    index_enhancement_strategy = StrategyNode(
        fund_id=75,
        parent_id=root_node.id,
        weight=0.5,
        name="指数增强策略",
        info=None,
        virtual_account=VirtualAccount(),
    )
    await index_enhancement_strategy.insert()


if __name__ == "__main__":
    asyncio.run(init_data())
