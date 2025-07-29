from pydantic import BaseModel

from src.database.orm.fund import Fund


class CreateFund(BaseModel):
    name: str


class UpdateFund(BaseModel):
    name: str


class CreateStrategyTree(BaseModel):
    name: str
    type: StrategyPortfolioTypeEnum
    weight: float
    info: dict


class FundService:
    def create_fund(self, data: CreateFund) -> Fund:
        fund = Fund.model_validate(data)
        fund.save()
        return fund

    def create_strategy_tree(self, fund_id: int, data: CreateStrategyTree) -> StrategyTree:
        pass
