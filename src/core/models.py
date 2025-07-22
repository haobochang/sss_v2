from datetime import datetime
from enum import Enum
from typing import Any, ClassVar, Self

from pydantic import BaseModel, Field
from pydantic_mongo import PydanticObjectId
from pymongo import MongoClient


def get_db():
    client = MongoClient("mongodb://virgo_user:k17o08m_Hgt4@mongotest01.sci-inv.cn:27017/admin")
    return client["hbc_test"]


class PositionType(str, Enum):
    """持仓类型枚举."""

    STOCK_LONG = "stock_long"  # 股票多头
    STOCK_SHORT = "stock_short"  # 股票空头
    FUTURE_LONG = "future_long"  # 期货多头（买入开仓）
    FUTURE_SHORT = "future_short"  # 期货空头（卖出开仓）
    OPTION = "option"  # 期权（预留）
    BOND = "bond"  # 债券（预留）


class AssetType(str, Enum):
    """资产类型枚举."""

    STOCK = "stock"  # 股票
    FUTURE = "future"  # 期货
    OPTION = "option"  # 期权
    BOND = "bond"  # 债券


class AccountType(str, Enum):
    """账户类型枚举."""

    STOCK = "stock"  # 股票账户
    FUTURE = "future"  # 期货账户
    OPTION = "option"  # 期权账户
    MARGIN = "margin"  # 融资融券账户


class FutureDirection(str, Enum):
    """期货方向枚举."""

    LONG = "long"  # 多头（买入）
    SHORT = "short"  # 空头（卖出）


class StrategyType(str, Enum):
    """策略类型枚举."""

    TREND_FOLLOWING = "trend_following"  # 趋势跟踪
    MEAN_REVERSION = "mean_reversion"  # 均值回归
    MOMENTUM = "momentum"  # 动量策略
    ARBITRAGE = "arbitrage"  # 套利策略
    MARKET_MAKING = "market_making"  # 做市策略
    STATISTICAL_ARBITRAGE = "stat_arb"  # 统计套利
    PAIRS_TRADING = "pairs_trading"  # 配对交易
    QUANTITATIVE = "quantitative"  # 量化策略
    FUNDAMENTAL = "fundamental"  # 基本面策略
    CUSTOM = "custom"  # 自定义策略


class StrategyStatus(str, Enum):
    """策略状态枚举."""

    INACTIVE = "inactive"  # 未激活
    ACTIVE = "active"  # 激活运行
    PAUSED = "paused"  # 暂停
    STOPPED = "stopped"  # 停止
    ERROR = "error"  # 错误状态


class OrderType(str, Enum):
    """订单类型枚举."""

    BUY = "buy"  # 买入
    SELL = "sell"  # 卖出
    BUY_OPEN = "buy_open"  # 买入开仓
    SELL_OPEN = "sell_open"  # 卖出开仓
    BUY_CLOSE = "buy_close"  # 买入平仓
    SELL_CLOSE = "sell_close"  # 卖出平仓


class OrderStatus(str, Enum):
    """订单状态枚举."""

    PENDING = "pending"  # 待执行
    PARTIAL = "partial"  # 部分成交
    FILLED = "filled"  # 完全成交
    CANCELLED = "cancelled"  # 已取消
    REJECTED = "rejected"  # 已拒绝


class BaseMongoModel(BaseModel):
    """基础MongoDB模型."""

    id: PydanticObjectId | None = Field(default=None, alias="_id")
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
    __abstract__ = True

    __collection__: ClassVar[str] = ""

    def insert(self) -> Self:
        if self.id is not None:
            # 有 id 的只能更新和删除，不能插入
            raise ValueError("有 id 的只能更新和删除，不能插入")
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        db = get_db()
        coll = db[self.__collection__]
        obj = self.model_dump(exclude_none=True, by_alias=True)
        doc = coll.insert_one(obj)
        self.id = doc.inserted_id
        return self

    def update(self) -> Self:
        if self.id is None:
            raise ValueError("没有 id 的只能插入，不能更新")
        self.updated_at = datetime.now()
        db = get_db()
        coll = db[self.__collection__]
        obj = self.model_dump(exclude_none=True, by_alias=True)
        coll.update_one({"_id": self.id}, {"$set": obj})
        return self

    def delete(self):
        if self.id is None:
            raise ValueError("没有 id 的只能插入，不能删除")
        db = get_db()
        coll = db[self.__collection__]
        coll.delete_one({"_id": self.id})

    @classmethod
    def find_by_id(cls, _id: PydanticObjectId) -> Self | None:
        db = get_db()
        coll = db[cls.__collection__]
        doc = coll.find_one({"_id": _id})
        if doc is None:
            return None
        return cls.model_validate(doc)

    @classmethod
    def get_collection(cls):
        db = get_db()
        return db[cls.__collection__]


class Account(BaseMongoModel):
    """账户实体模型."""

    __collection__ = "account"

    fund_id: int = Field(..., description="基金id")
    account_type: AccountType = Field(..., description="账户类型")
    account_name: str = Field(..., description="账户名称")
    account_code: str = Field(..., description="账户代码")

    # 资金信息
    total_assets: float = Field(default=0.0, description="总资产")
    available_funds: float = Field(default=0.0, description="可用资金")
    frozen_funds: float = Field(default=0.0, description="冻结资金")

    # 期货账户特有字段
    margin_used: float | None = Field(default=None, description="已用保证金")
    margin_available: float | None = Field(default=None, description="可用保证金")
    risk_ratio: float | None = Field(default=None, description="风险度")
    floating_pnl: float | None = Field(default=None, description="浮动盈亏")
    realized_pnl: float | None = Field(default=None, description="实现盈亏")

    @property
    def margin_ratio(self) -> float | None:
        """计算保证金比例."""
        if self.account_type != AccountType.FUTURE or not self.total_assets:
            return None
        if not self.margin_used:
            return 0.0
        return self.margin_used / self.total_assets

    @property
    def is_risky(self) -> bool:
        """判断是否存在风险（风险度超过80%）."""
        if not self.risk_ratio:
            return False
        return self.risk_ratio > 0.8


class FundPosition(BaseMongoModel):
    """基金持仓统一模型."""

    __collection__ = "fund_position"

    fund_id: int = Field(..., description="基金id")
    account_id: PydanticObjectId = Field(..., description="所属账户id")
    position_type: PositionType = Field(..., description="持仓类型")
    asset_type: AssetType = Field(..., description="资产类型")

    # 通用字段
    asset_name: str = Field(..., description="资产名称")
    asset_code: str = Field(..., description="资产代码")
    quantity: int = Field(..., description="数量")

    # 价格相关
    current_price: float = Field(..., description="当前价格")

    # 股票特有字段
    cost_price: float | None = Field(default=None, description="成本价（股票用）")

    # 期货特有字段
    open_price: float | None = Field(default=None, description="开仓价格（期货用）")
    direction: FutureDirection | None = Field(default=None, description="期货方向")
    contract_month: str | None = Field(default=None, description="合约月份（期货用）")
    contract_size: int | None = Field(default=None, description="合约乘数（期货用）")
    margin_per_lot: float | None = Field(default=None, description="每手保证金（期货用）")

    # 期权特有字段（预留）
    exercise_price: float | None = Field(default=None, description="行权价格（期权用）")
    expiry_date: datetime | None = Field(default=None, description="到期日期")

    @property
    def market_value(self) -> float:
        """计算市值."""
        if self.asset_type == AssetType.FUTURE and self.contract_size:
            return self.current_price * abs(self.quantity) * self.contract_size
        return self.current_price * abs(self.quantity)

    @property
    def cost_value(self) -> float:
        """计算成本价值."""
        if self.asset_type == AssetType.STOCK and self.cost_price:
            return self.cost_price * abs(self.quantity)
        elif self.asset_type == AssetType.FUTURE and self.open_price and self.contract_size:
            return self.open_price * abs(self.quantity) * self.contract_size
        return 0.0

    @property
    def unrealized_pnl(self) -> float:
        """计算浮动盈亏."""
        if self.asset_type == AssetType.STOCK and self.cost_price:
            # 股票盈亏
            pnl = (self.current_price - self.cost_price) * self.quantity
            return pnl
        elif self.asset_type == AssetType.FUTURE and self.open_price and self.direction:
            # 期货盈亏
            price_diff = self.current_price - self.open_price
            multiplier = self.contract_size or 1

            if self.direction == FutureDirection.LONG:
                # 多头：当前价格 > 开仓价格 = 盈利
                pnl = price_diff * abs(self.quantity) * multiplier
            else:
                # 空头：当前价格 < 开仓价格 = 盈利
                pnl = -price_diff * abs(self.quantity) * multiplier
            return pnl
        return 0.0

    @property
    def required_margin(self) -> float:
        """计算所需保证金（期货用）."""
        if self.asset_type == AssetType.FUTURE and self.margin_per_lot:
            return self.margin_per_lot * abs(self.quantity)
        return 0.0

    @property
    def is_long_position(self) -> bool:
        """判断是否为多头持仓."""
        return self.position_type in [PositionType.STOCK_LONG, PositionType.FUTURE_LONG]

    @property
    def is_short_position(self) -> bool:
        """判断是否为空头持仓."""
        return self.position_type in [PositionType.STOCK_SHORT, PositionType.FUTURE_SHORT]


class StrategyTemplate(BaseMongoModel):
    """策略模板."""

    __collection__ = "strategy_template"

    template_name: str = Field(..., description="模板名称")
    strategy_type: StrategyType = Field(..., description="策略类型")
    description: str | None = Field(default=None, description="策略描述")

    # 策略参数定义
    parameters: dict[str, Any] = Field(default_factory=dict, description="参数定义")
    default_config: dict[str, Any] = Field(default_factory=dict, description="默认配置")

    # 风控设置
    max_position_size: float | None = Field(default=None, description="最大持仓规模")
    max_daily_loss: float | None = Field(default=None, description="最大日损失")
    max_drawdown: float | None = Field(default=None, description="最大回撤")

    # 适用范围
    supported_assets: list[AssetType] = Field(default_factory=list, description="支持的资产类型")

    @property
    def is_stock_strategy(self) -> bool:
        """是否为股票策略."""
        return AssetType.STOCK in self.supported_assets

    @property
    def is_future_strategy(self) -> bool:
        """是否为期货策略."""
        return AssetType.FUTURE in self.supported_assets


class Strategy(BaseMongoModel):
    """策略实例."""

    __collection__ = "strategy"

    fund_id: int = Field(..., description="基金id")
    account_id: PydanticObjectId | None = Field(default=None, description="关联账户id")
    template_id: PydanticObjectId = Field(..., description="策略模板id")

    strategy_name: str = Field(..., description="策略实例名称")
    strategy_type: StrategyType = Field(..., description="策略类型")
    status: StrategyStatus = Field(default=StrategyStatus.INACTIVE, description="策略状态")

    # 策略配置
    config: dict[str, Any] = Field(default_factory=dict, description="策略配置参数")

    # 资金配置
    allocated_capital: float = Field(..., description="分配资金")
    max_position_size: float | None = Field(default=None, description="最大持仓规模")

    # 风控设置
    daily_loss_limit: float | None = Field(default=None, description="日损失限制")
    total_loss_limit: float | None = Field(default=None, description="总损失限制")
    max_drawdown_limit: float | None = Field(default=None, description="最大回撤限制")

    # 运行统计
    start_time: datetime | None = Field(default=None, description="启动时间")
    stop_time: datetime | None = Field(default=None, description="停止时间")
    total_trades: int = Field(default=0, description="总交易次数")
    winning_trades: int = Field(default=0, description="盈利交易次数")
    total_pnl: float = Field(default=0.0, description="总盈亏")
    max_drawdown: float = Field(default=0.0, description="最大回撤")

    def start(self) -> Self:
        """启动策略."""
        if self.status != StrategyStatus.INACTIVE:
            raise ValueError(f"策略状态为 {self.status.value}，无法启动")

        self.status = StrategyStatus.ACTIVE
        self.start_time = datetime.now()
        return self.update()

    def pause(self) -> Self:
        """暂停策略."""
        if self.status != StrategyStatus.ACTIVE:
            raise ValueError(f"策略状态为 {self.status.value}，无法暂停")

        self.status = StrategyStatus.PAUSED
        return self.update()

    def stop(self) -> Self:
        """停止策略."""
        if self.status in [StrategyStatus.INACTIVE, StrategyStatus.STOPPED]:
            raise ValueError(f"策略状态为 {self.status.value}，无法停止")

        self.status = StrategyStatus.STOPPED
        self.stop_time = datetime.now()
        return self.update()

    @property
    def win_rate(self) -> float:
        """胜率."""
        if self.total_trades == 0:
            return 0.0
        return self.winning_trades / self.total_trades

    @property
    def is_running(self) -> bool:
        """是否正在运行."""
        return self.status == StrategyStatus.ACTIVE

    @property
    def performance_summary(self) -> dict[str, Any]:
        """性能概要."""
        return {
            "total_trades": self.total_trades,
            "win_rate": self.win_rate,
            "total_pnl": self.total_pnl,
            "max_drawdown": self.max_drawdown,
            "allocated_capital": self.allocated_capital,
            "return_rate": self.total_pnl / self.allocated_capital
            if self.allocated_capital > 0
            else 0.0,
        }


class StrategyOrder(BaseMongoModel):
    """策略订单."""

    __collection__ = "strategy_order"

    strategy_id: PydanticObjectId = Field(..., description="策略id")
    fund_id: int = Field(..., description="基金id")
    account_id: PydanticObjectId = Field(..., description="账户id")

    # 订单信息
    order_type: OrderType = Field(..., description="订单类型")
    asset_type: AssetType = Field(..., description="资产类型")
    asset_code: str = Field(..., description="资产代码")
    asset_name: str = Field(..., description="资产名称")

    # 价格数量
    quantity: int = Field(..., description="委托数量")
    price: float | None = Field(default=None, description="委托价格（市价单为None）")
    filled_quantity: int = Field(default=0, description="成交数量")
    avg_filled_price: float | None = Field(default=None, description="平均成交价格")

    # 状态
    status: OrderStatus = Field(default=OrderStatus.PENDING, description="订单状态")
    order_time: datetime = Field(default_factory=datetime.now, description="委托时间")
    filled_time: datetime | None = Field(default=None, description="成交时间")

    # 策略信号
    signal_reason: str | None = Field(default=None, description="信号原因")

    @property
    def is_filled(self) -> bool:
        """是否完全成交."""
        return self.status == OrderStatus.FILLED

    @property
    def fill_ratio(self) -> float:
        """成交比例."""
        if self.quantity == 0:
            return 0.0
        return self.filled_quantity / self.quantity

    @property
    def total_amount(self) -> float:
        """总金额."""
        if self.avg_filled_price and self.filled_quantity:
            return self.avg_filled_price * self.filled_quantity
        return 0.0


class StrategyPerformance(BaseMongoModel):
    """策略性能记录."""

    __collection__ = "strategy_performance"

    strategy_id: PydanticObjectId = Field(..., description="策略id")
    date: datetime = Field(..., description="日期")

    # 资金指标
    nav: float = Field(..., description="净值")
    total_assets: float = Field(..., description="总资产")
    cash: float = Field(..., description="现金")
    position_value: float = Field(..., description="持仓市值")

    # 收益指标
    daily_return: float = Field(default=0.0, description="日收益率")
    cumulative_return: float = Field(default=0.0, description="累计收益率")
    max_drawdown: float = Field(default=0.0, description="最大回撤")

    # 交易指标
    trades_count: int = Field(default=0, description="当日交易次数")
    turnover: float = Field(default=0.0, description="换手率")

    # 风险指标
    volatility: float | None = Field(default=None, description="波动率")
    sharpe_ratio: float | None = Field(default=None, description="夏普比率")

    @classmethod
    def calculate_performance(cls, strategy_id: PydanticObjectId, date: datetime) -> Self:
        """计算策略性能."""
        # 这里应该包含实际的性能计算逻辑
        # 暂时返回示例数据
        return cls(
            strategy_id=strategy_id,
            date=date,
            nav=1.0,
            total_assets=1000000.0,
            cash=500000.0,
            position_value=500000.0,
        )


# 以下模型已弃用，建议使用 FundPosition 统一模型
class FundStockPosition(BaseMongoModel):
    """基金持仓实体模型.（已弃用，请使用 FundPosition）"""

    __collection__ = "fund_position_deprecated"
    fund_id: int = Field(..., description="基金id")
    stock_name: str = Field(..., description="股票名称")
    stock_code: str = Field(..., description="股票代码")
    price: float = Field(..., description="股票价格")
    quantity: int = Field(..., description="股票数量")


class FundFuturePosition(BaseMongoModel):
    """基金期货持仓实体模型.（已弃用，请使用 FundPosition）"""

    __collection__ = "fund_future_position_deprecated"
    fund_id: int = Field(..., description="基金id")
    future_name: str = Field(..., description="期货名称")
    future_code: str = Field(..., description="期货代码")


class Fund(BaseMongoModel):
    """基金实体模型."""

    __collection__ = "fund"

    fund_id: int = Field(..., description="基金id")
    fund_name: str = Field(..., description="基金名称")
    fund_code: str = Field(..., description="基金代码")

    def get_accounts(self, account_type: AccountType | None = None) -> list[Account]:
        """获取基金账户."""
        db = get_db()
        coll = db[Account.__collection__]

        query = {"fund_id": self.fund_id}
        if account_type:
            query["account_type"] = account_type.value

        docs = coll.find(query)
        return [Account.model_validate(doc) for doc in docs]

    def get_strategies(self, status: StrategyStatus | None = None) -> list[Strategy]:
        """获取基金策略."""
        db = get_db()
        coll = db[Strategy.__collection__]

        query = {"fund_id": self.fund_id}
        if status:
            query["status"] = status.value

        docs = coll.find(query)
        return [Strategy.model_validate(doc) for doc in docs]

    def get_active_strategies(self) -> list[Strategy]:
        """获取活跃策略."""
        return self.get_strategies(StrategyStatus.ACTIVE)

    def get_strategy_orders(
        self, strategy_id: PydanticObjectId | None = None, status: OrderStatus | None = None
    ) -> list[StrategyOrder]:
        """获取策略订单."""
        db = get_db()
        coll = db[StrategyOrder.__collection__]

        query = {"fund_id": self.fund_id}
        if strategy_id:
            query["strategy_id"] = strategy_id
        if status:
            query["status"] = status.value

        docs = coll.find(query)
        return [StrategyOrder.model_validate(doc) for doc in docs]

    def get_positions(
        self, account_id: PydanticObjectId | None = None, position_type: PositionType | None = None
    ) -> list[FundPosition]:
        """获取基金持仓."""
        db = get_db()
        coll = db[FundPosition.__collection__]

        query = {"fund_id": self.fund_id}
        if account_id:
            query["account_id"] = account_id
        if position_type:
            query["position_type"] = position_type.value

        docs = coll.find(query)
        return [FundPosition.model_validate(doc) for doc in docs]

    def get_stock_positions(
        self, long_only: bool = False, short_only: bool = False
    ) -> list[FundPosition]:
        """获取股票持仓."""
        db = get_db()
        coll = db[FundPosition.__collection__]

        query = {"fund_id": self.fund_id, "asset_type": AssetType.STOCK.value}

        if long_only:
            query["position_type"] = PositionType.STOCK_LONG.value
        elif short_only:
            query["position_type"] = PositionType.STOCK_SHORT.value

        docs = coll.find(query)
        return [FundPosition.model_validate(doc) for doc in docs]

    def get_future_positions(self, direction: FutureDirection | None = None) -> list[FundPosition]:
        """获取期货持仓."""
        db = get_db()
        coll = db[FundPosition.__collection__]

        query = {"fund_id": self.fund_id, "asset_type": AssetType.FUTURE.value}
        if direction:
            query["direction"] = direction.value

        docs = coll.find(query)
        return [FundPosition.model_validate(doc) for doc in docs]

    def total_market_value(self) -> float:
        """计算总市值."""
        positions = self.get_positions()
        return sum(pos.market_value for pos in positions)

    def total_unrealized_pnl(self) -> float:
        """计算总浮动盈亏."""
        positions = self.get_positions()
        return sum(pos.unrealized_pnl for pos in positions)

    def stock_market_value(self) -> float:
        """计算股票市值."""
        stock_positions = self.get_stock_positions()
        return sum(pos.market_value for pos in stock_positions)

    def future_market_value(self) -> float:
        """计算期货市值."""
        future_positions = self.get_future_positions()
        return sum(pos.market_value for pos in future_positions)

    def future_required_margin(self) -> float:
        """计算期货所需保证金."""
        future_positions = self.get_future_positions()
        return sum(pos.required_margin for pos in future_positions)

    def get_risk_summary(self) -> dict:
        """获取风险概览."""
        future_accounts = self.get_accounts(AccountType.FUTURE)

        summary = {
            "total_risk_ratio": 0.0,
            "risky_accounts": 0,
            "total_margin_used": 0.0,
            "total_floating_pnl": 0.0,
        }

        for account in future_accounts:
            if account.risk_ratio:
                summary["total_risk_ratio"] = max(summary["total_risk_ratio"], account.risk_ratio)
            if account.is_risky:
                summary["risky_accounts"] += 1
            if account.margin_used:
                summary["total_margin_used"] += account.margin_used
            if account.floating_pnl:
                summary["total_floating_pnl"] += account.floating_pnl

        return summary

    def get_strategies_summary(self) -> dict[str, Any]:
        """获取策略概要."""
        strategies = self.get_strategies()
        active_strategies = self.get_active_strategies()

        total_allocated = sum(s.allocated_capital for s in strategies)
        total_pnl = sum(s.total_pnl for s in strategies)

        return {
            "total_strategies": len(strategies),
            "active_strategies": len(active_strategies),
            "total_allocated_capital": total_allocated,
            "total_strategy_pnl": total_pnl,
            "average_return": total_pnl / total_allocated if total_allocated > 0 else 0.0,
        }


if __name__ == "__main__":
    from rich import print as rprint

    # 清理数据
    Fund.get_collection().delete_many({})
    Account.get_collection().delete_many({})
    FundPosition.get_collection().delete_many({})
    StrategyTemplate.get_collection().delete_many({})
    Strategy.get_collection().delete_many({})
    StrategyOrder.get_collection().delete_many({})
    StrategyPerformance.get_collection().delete_many({})

    # 创建基金
    fund = Fund(fund_id=1, fund_name="测试基金", fund_code="123456")
    rprint("创建基金:", fund.fund_name)
    fund.insert()

    # 创建账户
    stock_account = Account(
        fund_id=fund.fund_id,
        account_type=AccountType.STOCK,
        account_name="股票账户",
        account_code="STOCK001",
        total_assets=2000000.0,
        available_funds=1500000.0,
        frozen_funds=0.0,
    )
    stock_account.insert()

    future_account = Account(
        fund_id=fund.fund_id,
        account_type=AccountType.FUTURE,
        account_name="期货账户",
        account_code="FUTURE001",
        total_assets=3000000.0,
        available_funds=2200000.0,
        margin_used=800000.0,
        margin_available=1400000.0,
        risk_ratio=0.27,
        floating_pnl=25000.0,
        realized_pnl=15000.0,
    )
    future_account.insert()

    # 创建策略模板
    momentum_template = StrategyTemplate(
        template_name="动量策略模板",
        strategy_type=StrategyType.MOMENTUM,
        description="基于动量因子的量化策略",
        parameters={
            "lookback_period": {"type": "int", "default": 20, "min": 5, "max": 60},
            "momentum_threshold": {"type": "float", "default": 0.02, "min": 0.01, "max": 0.1},
            "position_size": {"type": "float", "default": 0.1, "min": 0.05, "max": 0.5},
        },
        default_config={"lookback_period": 20, "momentum_threshold": 0.02, "position_size": 0.1},
        max_position_size=500000.0,
        max_daily_loss=50000.0,
        max_drawdown=0.15,
        supported_assets=[AssetType.STOCK],
    )
    momentum_template.insert()

    arbitrage_template = StrategyTemplate(
        template_name="套利策略模板",
        strategy_type=StrategyType.ARBITRAGE,
        description="期货套利策略",
        parameters={
            "spread_threshold": {"type": "float", "default": 10.0, "min": 5.0, "max": 50.0},
            "max_positions": {"type": "int", "default": 5, "min": 1, "max": 10},
            "leverage": {"type": "float", "default": 3.0, "min": 1.0, "max": 5.0},
        },
        default_config={"spread_threshold": 10.0, "max_positions": 5, "leverage": 3.0},
        max_position_size=1000000.0,
        max_daily_loss=100000.0,
        max_drawdown=0.2,
        supported_assets=[AssetType.FUTURE],
    )
    arbitrage_template.insert()

    # 创建策略实例
    momentum_strategy = Strategy(
        fund_id=fund.fund_id,
        account_id=stock_account.id,  # type: ignore
        template_id=momentum_template.id,  # type: ignore
        strategy_name="股票动量策略A",
        strategy_type=StrategyType.MOMENTUM,
        allocated_capital=800000.0,
        config={"lookback_period": 15, "momentum_threshold": 0.025, "position_size": 0.12},
        daily_loss_limit=30000.0,
        total_loss_limit=150000.0,
        max_drawdown_limit=0.12,
    )
    momentum_strategy.insert()

    arbitrage_strategy = Strategy(
        fund_id=fund.fund_id,
        account_id=future_account.id,  # type: ignore
        template_id=arbitrage_template.id,  # type: ignore
        strategy_name="期货套利策略B",
        strategy_type=StrategyType.ARBITRAGE,
        allocated_capital=1200000.0,
        config={"spread_threshold": 8.0, "max_positions": 3, "leverage": 2.5},
        daily_loss_limit=60000.0,
        total_loss_limit=240000.0,
        max_drawdown_limit=0.18,
    )
    arbitrage_strategy.insert()

    # 启动策略
    rprint(f"\n=== 启动策略 ===")
    momentum_strategy.start()
    arbitrage_strategy.start()
    rprint(f"动量策略状态: {momentum_strategy.status.value}")
    rprint(f"套利策略状态: {arbitrage_strategy.status.value}")

    # 模拟策略订单
    # 动量策略订单
    order1 = StrategyOrder(
        strategy_id=momentum_strategy.id,  # type: ignore
        fund_id=fund.fund_id,
        account_id=stock_account.id,  # type: ignore
        order_type=OrderType.BUY,
        asset_type=AssetType.STOCK,
        asset_code="000001",
        asset_name="平安银行",
        quantity=5000,
        price=10.80,
        filled_quantity=5000,
        avg_filled_price=10.78,
        status=OrderStatus.FILLED,
        signal_reason="动量信号触发买入",
    )
    order1.insert()

    # 套利策略订单
    order2 = StrategyOrder(
        strategy_id=arbitrage_strategy.id,  # type: ignore
        fund_id=fund.fund_id,
        account_id=future_account.id,  # type: ignore
        order_type=OrderType.BUY_OPEN,
        asset_type=AssetType.FUTURE,
        asset_code="IF2412",
        asset_name="沪深300期货",
        quantity=3,
        price=3850.0,
        filled_quantity=3,
        avg_filled_price=3848.0,
        status=OrderStatus.FILLED,
        signal_reason="价差扩大，做多主力合约",
    )
    order2.insert()

    order3 = StrategyOrder(
        strategy_id=arbitrage_strategy.id,  # type: ignore
        fund_id=fund.fund_id,
        account_id=future_account.id,  # type: ignore
        order_type=OrderType.SELL_OPEN,
        asset_type=AssetType.FUTURE,
        asset_code="IF2403",
        asset_name="沪深300期货远月",
        quantity=3,
        price=3870.0,
        filled_quantity=3,
        avg_filled_price=3872.0,
        status=OrderStatus.FILLED,
        signal_reason="价差扩大，做空远月合约",
    )
    order3.insert()

    # 创建持仓（基于订单）
    stock_position = FundPosition(
        fund_id=fund.fund_id,
        account_id=stock_account.id,  # type: ignore
        position_type=PositionType.STOCK_LONG,
        asset_type=AssetType.STOCK,
        asset_name="平安银行",
        asset_code="000001",
        current_price=10.95,
        cost_price=10.78,
        quantity=5000,
    )
    stock_position.insert()

    future_long_position = FundPosition(
        fund_id=fund.fund_id,
        account_id=future_account.id,  # type: ignore
        position_type=PositionType.FUTURE_LONG,
        asset_type=AssetType.FUTURE,
        asset_name="沪深300期货",
        asset_code="IF2412",
        current_price=3860.0,
        open_price=3848.0,
        quantity=3,
        direction=FutureDirection.LONG,
        contract_month="2024-12",
        contract_size=300,
        margin_per_lot=46000.0,
    )
    future_long_position.insert()

    future_short_position = FundPosition(
        fund_id=fund.fund_id,
        account_id=future_account.id,  # type: ignore
        position_type=PositionType.FUTURE_SHORT,
        asset_type=AssetType.FUTURE,
        asset_name="沪深300期货远月",
        asset_code="IF2403",
        current_price=3865.0,
        open_price=3872.0,
        quantity=3,
        direction=FutureDirection.SHORT,
        contract_month="2024-03",
        contract_size=300,
        margin_per_lot=46000.0,
    )
    future_short_position.insert()

    # 更新策略统计
    momentum_strategy.total_trades = 1
    momentum_strategy.winning_trades = 1
    momentum_strategy.total_pnl = 8500.0  # (10.95 - 10.78) * 5000
    momentum_strategy.update()

    arbitrage_strategy.total_trades = 2
    arbitrage_strategy.winning_trades = 1
    arbitrage_strategy.total_pnl = 4200.0  # 套利盈亏
    arbitrage_strategy.update()

    # === 策略分析和展示 ===
    rprint(f"\n{'=' * 50}")
    rprint(f"📊 策略配置体系演示")
    rprint(f"{'=' * 50}")

    # 策略模板信息
    rprint(f"\n🎯 策略模板:")
    rprint(f"动量策略模板: {momentum_template.template_name}")
    rprint(f"  支持资产: {[asset.value for asset in momentum_template.supported_assets]}")
    rprint(f"  参数配置: {momentum_template.default_config}")

    rprint(f"套利策略模板: {arbitrage_template.template_name}")
    rprint(f"  支持资产: {[asset.value for asset in arbitrage_template.supported_assets]}")
    rprint(f"  参数配置: {arbitrage_template.default_config}")

    # 策略实例状态
    rprint(f"\n🚀 策略实例状态:")
    active_strategies = fund.get_active_strategies()
    for strategy in active_strategies:
        perf = strategy.performance_summary
        rprint(f"{strategy.strategy_name}:")
        rprint(f"  状态: {strategy.status.value}")
        rprint(f"  分配资金: {strategy.allocated_capital:,.0f}")
        rprint(f"  总交易: {perf['total_trades']}笔")
        rprint(f"  胜率: {perf['win_rate']:.1%}")
        rprint(f"  总盈亏: {perf['total_pnl']:+,.0f}")
        rprint(f"  收益率: {perf['return_rate']:+.2%}")

    # 策略订单
    rprint(f"\n📋 策略订单:")
    all_orders = fund.get_strategy_orders()
    for order in all_orders:
        rprint(f"{order.asset_name} ({order.order_type.value}):")
        rprint(f"  数量: {order.quantity}, 价格: {order.price}")
        rprint(f"  成交: {order.filled_quantity}@{order.avg_filled_price}")
        rprint(f"  状态: {order.status.value}")
        rprint(f"  信号: {order.signal_reason}")

    # 持仓详情
    rprint(f"\n💼 当前持仓:")
    all_positions = fund.get_positions()
    for pos in all_positions:
        rprint(f"{pos.asset_name} ({pos.position_type.value}):")
        rprint(f"  数量: {pos.quantity}手")
        rprint(f"  当前价: {pos.current_price}")
        if pos.asset_type == AssetType.STOCK:
            rprint(f"  成本价: {pos.cost_price}")
        else:
            rprint(f"  开仓价: {pos.open_price}")
            rprint(f"  方向: {pos.direction.value if pos.direction else 'N/A'}")
        rprint(f"  市值: {pos.market_value:,.0f}")
        rprint(f"  盈亏: {pos.unrealized_pnl:+,.0f}")

    # 基金总体概况
    rprint(f"\n📈 基金总体概况:")
    rprint(f"总市值: {fund.total_market_value():,.0f}")
    rprint(f"总浮动盈亏: {fund.total_unrealized_pnl():+,.0f}")

    # 策略概要
    strategy_summary = fund.get_strategies_summary()
    rprint(f"\n🎯 策略概要:")
    rprint(f"策略总数: {strategy_summary['total_strategies']}")
    rprint(f"运行中策略: {strategy_summary['active_strategies']}")
    rprint(f"分配资金: {strategy_summary['total_allocated_capital']:,.0f}")
    rprint(f"策略总盈亏: {strategy_summary['total_strategy_pnl']:+,.0f}")
    rprint(f"平均收益率: {strategy_summary['average_return']:+.2%}")

    # 风险监控
    risk_summary = fund.get_risk_summary()
    rprint(f"\n⚠️  风险监控:")
    rprint(f"最高风险度: {risk_summary['total_risk_ratio']:.1%}")
    rprint(f"风险账户数: {risk_summary['risky_accounts']}")
    rprint(f"期货保证金: {risk_summary['total_margin_used']:,.0f}")

    # 策略管理操作演示
    rprint(f"\n🔧 策略管理演示:")
    rprint("暂停动量策略...")
    momentum_strategy.pause()
    rprint(f"动量策略状态: {momentum_strategy.status.value}")

    # 展示暂停后的活跃策略数量
    active_count = len(fund.get_active_strategies())
    rprint(f"当前活跃策略数: {active_count}")
