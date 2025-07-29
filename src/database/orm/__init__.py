from beanie import init_beanie
from pymongo import AsyncMongoClient

from .fund import Fund, StrategyTree
from .strategy import StrategyNode

__all__ = ["Fund", "StrategyNode", "StrategyTree"]


async def register_orm_models():
    client = AsyncMongoClient("mongodb://localhost:27017")
    db = client["hbc_test"]
    await init_beanie(
        db,
        document_models=[
            Fund,
            StrategyNode,
            StrategyTree,
        ],
    )
