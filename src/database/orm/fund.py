import pymongo
from beanie import Indexed
from pydantic import Field

from ._base import BaseDocument


class Fund(BaseDocument):
    fund_id: int = Field(..., description="基金id")
    name: str = Field(..., description="基金名称")
    code: str = Field(..., description="基金代码")

    class Settings:
        name = "fund"
        indexes = [
            pymongo.IndexModel("fund_id", unique=True),
            pymongo.IndexModel("name"),
            pymongo.IndexModel("code"),
        ]


class StrategyTree(BaseDocument):
    fund_id: int = Indexed(int)
