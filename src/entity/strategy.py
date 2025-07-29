from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class TradeDirection(str, Enum):
    """交易方向"""

    BUY = "BUY"
    SELL = "SELL"


class TradeOrder(BaseModel):
    """交易单"""

    strategy_name: str = Field(description="策略名称")
    stock_code: str = Field(description="股票代码")
    direction: TradeDirection = Field(description="交易方向")
    target_shares: float = Field(description="目标股数")
    target_value: float = Field(description="目标金额")
    price: float = Field(description="价格")
    priority: int = Field(default=1, description="优先级，1最高")
    executed_shares: float = Field(default=0, description="已成交股数")
    executed_value: float = Field(default=0, description="已成交金额")

    @property
    def remaining_shares(self) -> float:
        return self.target_shares - self.executed_shares

    @property
    def remaining_value(self) -> float:
        return self.target_value - self.executed_value

    @property
    def execution_ratio(self) -> float:
        """成交比例"""
        return self.executed_shares / self.target_shares if self.target_shares > 0 else 0


class TradeOptimizer(BaseModel):
    """交易优化器"""

    def generate_target_weights(
        self, strategy: "StrategyTree", market_signal: dict
    ) -> dict[str, float]:
        """基于市场信号生成目标权重"""
        current_allocations = strategy._calculate_current_allocations()

        # 模拟优化器调整权重
        target_weights = current_allocations.copy()

        for stock_code, adjustment in market_signal.items():
            if stock_code in target_weights:
                new_weight = max(0, min(1, target_weights[stock_code] + adjustment))
                target_weights[stock_code] = new_weight

        # 归一化权重
        total_weight = sum(target_weights.values())
        if total_weight > 0:
            target_weights = {k: v / total_weight for k, v in target_weights.items()}

        return target_weights

    def generate_trade_orders(
        self, strategy: "StrategyTree", target_weights: dict[str, float]
    ) -> list[TradeOrder]:
        """生成交易单"""
        orders = []
        total_value = strategy._calculate_total_position_value()
        current_allocations = strategy._calculate_current_allocations()

        for stock_code, target_weight in target_weights.items():
            current_weight = current_allocations.get(stock_code, 0)
            weight_diff = target_weight - current_weight

            if abs(weight_diff) > 0.001:  # 忽略微小差异
                target_value = total_value * weight_diff
                stock_price = strategy._get_stock_price(stock_code)
                target_shares = abs(target_value) / stock_price

                direction = TradeDirection.BUY if weight_diff > 0 else TradeDirection.SELL

                order = TradeOrder(
                    strategy_name=strategy.name,
                    stock_code=stock_code,
                    direction=direction,
                    target_shares=target_shares,
                    target_value=abs(target_value),
                    price=stock_price,
                    priority=1,
                )
                orders.append(order)

        return orders


class TradingSystem(BaseModel):
    """交易系统"""

    execution_rate: float = Field(default=0.8, description="平均成交率")
    slippage_rate: float = Field(default=0.001, description="滑点率")

    def execute_orders(
        self, orders: list[TradeOrder], available_cash: float
    ) -> tuple[list[TradeOrder], float]:
        """
        执行交易单
        返回：(已执行的订单列表, 剩余现金)
        """
        executed_orders = []
        remaining_cash = available_cash

        # 按优先级排序，买单需要现金，优先处理卖单
        sell_orders = [o for o in orders if o.direction == TradeDirection.SELL]
        buy_orders = [o for o in orders if o.direction == TradeDirection.BUY]

        # 先执行卖单获得现金
        for order in sell_orders:
            execution_ratio = min(self.execution_rate, 1.0)
            executed_shares = order.target_shares * execution_ratio
            # 考虑滑点
            actual_price = order.price * (1 - self.slippage_rate)
            executed_value = executed_shares * actual_price

            order.executed_shares = executed_shares
            order.executed_value = executed_value
            remaining_cash += executed_value
            executed_orders.append(order)

        # 再执行买单
        for order in buy_orders:
            # 考虑滑点
            actual_price = order.price * (1 + self.slippage_rate)
            max_affordable_shares = remaining_cash / actual_price
            execution_ratio = min(self.execution_rate, 1.0)

            # 实际成交数量受现金限制
            target_executable = order.target_shares * execution_ratio
            executed_shares = min(target_executable, max_affordable_shares)
            executed_value = executed_shares * actual_price

            if executed_shares > 0.01:  # 最小成交单位
                order.executed_shares = executed_shares
                order.executed_value = executed_value
                remaining_cash -= executed_value
                executed_orders.append(order)

        return executed_orders, remaining_cash

    def cross_trade(self, orders: list[TradeOrder]) -> list[TradeOrder]:
        """内部自成交"""
        crossed_orders = []
        buy_orders = [o for o in orders if o.direction == TradeDirection.BUY]
        sell_orders = [o for o in orders if o.direction == TradeDirection.SELL]

        # 按股票代码匹配买卖单
        for buy_order in buy_orders:
            for sell_order in sell_orders:
                if (
                    buy_order.stock_code == sell_order.stock_code
                    and buy_order.remaining_shares > 0
                    and sell_order.remaining_shares > 0
                ):
                    # 计算可成交数量
                    cross_shares = min(buy_order.remaining_shares, sell_order.remaining_shares)
                    cross_price = (buy_order.price + sell_order.price) / 2  # 中间价成交
                    cross_value = cross_shares * cross_price

                    # 更新买单
                    buy_order.executed_shares += cross_shares
                    buy_order.executed_value += cross_value

                    # 更新卖单
                    sell_order.executed_shares += cross_shares
                    sell_order.executed_value += cross_value

        return orders


class StrategyPortfolioTypeEnum(str, Enum):
    """策略组合类型"""

    # 现金
    CASH = "CASH"
    # 指数增强
    INDEX_ENHANCEMENT = "INDEX_ENHANCEMENT"
    # 期货对冲
    HEDGING = "HEDGING"
    # 多空
    LONG_SHORT = "LONG_SHORT"
    # 灵活对冲
    FLEXIBLE_HEDGING = "FLEXIBLE_HEDGING"
    # 高频择时策略
    HIGH_FREQUENCY_TIMING = "HIGH_FREQUENCY_TIMING"


class CashInfo(BaseModel):
    """
    当存在待申购金额时，调仓的时候买入消耗待申购金额，直到消耗完
    当待申购金额为0时，调仓的时候买入消耗可用现金，直到消耗完
    当待申购金额为负时，调仓需要卖出，来使待申购金额为0，剩下的放在可用现金中
    """

    # 可用现金
    available_cash: float = Field(default=0, description="可用现金")
    # 待申购金额
    pending_purchase_amount: float = Field(
        default=0, description="待申购金额， 正数表示申购， 负数表示赎回"
    )


class StockPositionInfo(BaseModel):
    """
    股票持仓信息
    """

    # 股票代码
    stock_code: str = Field(description="股票代码")
    # 股票数量
    stock_amount: float = Field(description="股票数量")
    # 股票成本
    stock_cost: float = Field(description="股票成本")


class FuturesPositionInfo(BaseModel):
    """
    期货持仓信息
    """

    # 期货代码
    futures_code: str = Field(description="期货代码")
    # 期货数量
    futures_amount: float = Field(description="期货数量")
    # 期货成本
    futures_cost: float = Field(description="期货成本")


# 虚拟账户
class VirtualAccount(BaseModel):
    stock_long_info: list[StockPositionInfo] = Field(
        default_factory=list, description="股票多头信息"
    )
    stock_short_info: list[StockPositionInfo] = Field(
        default_factory=list, description="股票空头信息"
    )
    futures_long_info: list[FuturesPositionInfo] = Field(
        default_factory=list, description="期货多头信息"
    )
    futures_short_info: list[FuturesPositionInfo] = Field(
        default_factory=list, description="期货空头信息"
    )
    cash_info: CashInfo = Field(default=CashInfo(), description="现金信息")


class StrategyPortfolio(BaseModel):
    type: StrategyPortfolioTypeEnum
    name: str


class StrategyTree(BaseModel):
    """策略树"""

    fund_id: int
    weight: float
    name: str
    children: list["StrategyTree"] = Field(default_factory=list)
    virtual_account: VirtualAccount = Field(default_factory=VirtualAccount)
    strategy_info: dict = Field(default_factory=dict)

    def allocate_pending_amount(self, amount: float) -> None:
        """
        分配待申购金额：只在根节点记录，通过权重分配到叶子节点
        """
        if not self.children:
            # 叶子节点：接收分配的金额
            self.virtual_account.cash_info.pending_purchase_amount += amount
        else:
            # 非叶子节点：递归分配到子节点
            for child in self.children:
                child.allocate_pending_amount(amount * child.weight)

    def validate_weights(self, tolerance: float = 1e-6) -> bool:
        """验证同一层级子节点权重之和是否为1"""
        if not self.children:
            return True  # 叶子节点无需验证

        total_weight = sum(child.weight for child in self.children)
        if abs(total_weight - 1.0) > tolerance:
            raise ValueError(f"子节点权重之和不为1: {total_weight}")

        return all(child.validate_weights(tolerance) for child in self.children)

    def process_subscription(self, amount: float) -> None:
        """
        处理申购：只能在根节点调用，分配到所有策略（包括期货）
        """
        if self.weight != 1.0:
            raise ValueError("申购只能在根节点执行")

        # 根节点记录总申购金额
        self.virtual_account.cash_info.pending_purchase_amount += amount

        # 分配到所有叶子节点（包括期货策略）
        self._allocate_to_all_leaves(amount)
        print(f"申购 {amount:,.2f} 元到 {self.name}，已分配到各策略（包括期货）")

    def _allocate_to_all_leaves(self, amount: float) -> None:
        """分配到所有叶子节点，包括期货策略"""
        if not self.children:
            # 叶子节点：接收分配的金额
            self.virtual_account.cash_info.pending_purchase_amount += amount
        else:
            # 非叶子节点：递归分配到子节点
            for child in self.children:
                child._allocate_to_all_leaves(amount * child.weight)

    def process_redemption(self, amount: float) -> None:
        """
        处理赎回：只能在根节点调用
        """
        if self.weight != 1.0:
            raise ValueError("赎回只能在根节点执行")

        print(f"客户赎回: {amount:,.2f} 元")

        # 1. 先平仓期货释放保证金
        self._liquidate_futures_for_redemption()

        # 2. 计算需要卖出的股票
        self._liquidate_stocks_for_redemption(amount)

        # 3. 从根节点现金支付赎回款
        if self.virtual_account.cash_info.available_cash >= amount:
            self.virtual_account.cash_info.available_cash -= amount
            print(f"赎回完成，支付 {amount:,.2f} 元")
        else:
            available = self.virtual_account.cash_info.available_cash
            print(f"现金不足，只能赎回 {available:,.2f} 元")
            self.virtual_account.cash_info.available_cash = 0

    def _liquidate_futures_for_redemption(self) -> None:
        """为赎回平仓期货"""
        print("\n为赎回平仓期货...")

        def liquidate_node_futures(node):
            if not node.children and node._is_futures_strategy():
                if node.virtual_account.futures_short_info:
                    futures_info = node._get_futures_contract_info()
                    contract_value = futures_info["current_price"] * futures_info["multiplier"]

                    total_margin_released = 0
                    for position in node.virtual_account.futures_short_info:
                        position_value = position.futures_amount * contract_value
                        margin = position_value * futures_info["margin_rate"]
                        total_margin_released += margin

                    # 清空期货持仓
                    node.virtual_account.futures_short_info.clear()
                    node.virtual_account.cash_info.available_cash += total_margin_released
                    print(f"  {node.name}: 平仓期货，释放保证金 {total_margin_released:,.2f} 元")
            else:
                for child in node.children:
                    liquidate_node_futures(child)

        liquidate_node_futures(self)

    def _liquidate_stocks_for_redemption(self, redemption_amount: float) -> None:
        """为赎回卖出股票"""
        print(f"\n为赎回卖出股票，目标金额: {redemption_amount:,.2f} 元")

        # 收集所有叶子节点的股票持仓
        total_stock_value = 0
        stock_nodes = []

        def collect_stock_nodes(node):
            nonlocal total_stock_value
            if not node.children and not node._is_futures_strategy():
                node_stock_value = 0
                for position in node.virtual_account.stock_long_info:
                    stock_price = node._get_stock_price(position.stock_code)
                    position_value = position.stock_amount * stock_price
                    node_stock_value += position_value

                if node_stock_value > 0:
                    stock_nodes.append((node, node_stock_value))
                    total_stock_value += node_stock_value
            else:
                for child in node.children:
                    collect_stock_nodes(child)

        collect_stock_nodes(self)

        if total_stock_value == 0:
            print("  无股票持仓可卖出")
            return

        # 按比例卖出股票
        for node, node_stock_value in stock_nodes:
            sell_ratio = min(redemption_amount / total_stock_value, 1.0)
            node_sell_value = node_stock_value * sell_ratio

            cash_received = 0
            positions_to_remove = []

            for i, position in enumerate(node.virtual_account.stock_long_info):
                stock_price = node._get_stock_price(position.stock_code)
                position_value = position.stock_amount * stock_price

                if node_sell_value > 0:
                    sell_amount = min(position.stock_amount, node_sell_value / stock_price)
                    sell_value = sell_amount * stock_price

                    position.stock_amount -= sell_amount
                    node_sell_value -= sell_value
                    cash_received += sell_value

                    if position.stock_amount <= 0.01:  # 基本清仓
                        positions_to_remove.append(i)

            # 移除清仓的持仓
            for i in reversed(positions_to_remove):
                node.virtual_account.stock_long_info.pop(i)

            node.virtual_account.cash_info.available_cash += cash_received
            print(f"  {node.name}: 卖出股票获得现金 {cash_received:,.2f} 元")

    def build_positions_from_pending(
        self, strategy_allocations: dict[str, dict[str, float]] | None = None
    ) -> None:
        """
        从待申购金额建仓
        strategy_allocations: {"strategy_name": {"stock_code": allocation_ratio, ...}, ...}
        """
        if not self.children:
            # 叶子节点：执行建仓
            pending_amount = self.virtual_account.cash_info.pending_purchase_amount

            if pending_amount <= 0:
                return

            stock_allocations = (
                strategy_allocations.get(self.name) if strategy_allocations else None
            )

            if not stock_allocations:
                # 没有指定股票分配，转为可用现金
                self.virtual_account.cash_info.available_cash += pending_amount
                self.virtual_account.cash_info.pending_purchase_amount = 0
                print(f"{self.name}: 转移 {pending_amount:,.2f} 元到可用现金")
            else:
                # 按指定分配买入股票
                total_ratio = sum(stock_allocations.values())
                if abs(total_ratio - 1.0) > 1e-6:
                    raise ValueError(f"股票分配比例之和不为1: {total_ratio}")

                for stock_code, ratio in stock_allocations.items():
                    position_value = pending_amount * ratio
                    # 使用真实股票价格
                    stock_price = self._get_stock_price(stock_code)
                    shares = position_value / stock_price

                    position = StockPositionInfo(
                        stock_code=stock_code, stock_amount=shares, stock_cost=stock_price
                    )
                    self.virtual_account.stock_long_info.append(position)
                    print(
                        f"{self.name}: 买入 {stock_code} {shares:,.0f}股，成本 {stock_price:.2f}元/股"
                    )

                # 清零待申购金额
                self.virtual_account.cash_info.pending_purchase_amount = 0
        else:
            # 非叶子节点：清零当前节点的待申购金额，递归处理子节点
            self.virtual_account.cash_info.pending_purchase_amount = 0

            for child in self.children:
                child.build_positions_from_pending(strategy_allocations)

    def rebalance_positions(self, strategy_allocations: dict[str, dict[str, float]]) -> None:
        """
        调仓：根据新的分配比例调整持仓
        strategy_allocations: {"strategy_name": {"stock_code": target_ratio, ...}, ...}
        """
        if not self.children:
            # 叶子节点执行调仓
            new_allocations = strategy_allocations.get(self.name)
            if not new_allocations:
                print(f"{self.name}: 无调仓配置，跳过")
                return

            total_value = self._calculate_total_position_value()
            if total_value <= 0:
                print(f"{self.name}: 无持仓，跳过调仓")
                return

            current_allocations = self._calculate_current_allocations()

            print(f"\n{self.name} 调仓:")
            print(f"  总持仓价值: {total_value:,.2f} 元")
            print(f"  当前配置: {current_allocations}")
            print(f"  目标配置: {new_allocations}")

            # 计算需要买卖的数量
            for stock_code, target_ratio in new_allocations.items():
                target_value = total_value * target_ratio
                current_value = sum(
                    pos.stock_amount * self._get_stock_price(pos.stock_code)
                    for pos in self.virtual_account.stock_long_info
                    if pos.stock_code == stock_code
                )

                diff_value = target_value - current_value
                stock_price = self._get_stock_price(stock_code)  # 使用真实价格

                if abs(diff_value) > 1:  # 忽略小额差异
                    if diff_value > 0:
                        # 需要买入
                        shares_to_buy = diff_value / stock_price
                        position = StockPositionInfo(
                            stock_code=stock_code,
                            stock_amount=shares_to_buy,
                            stock_cost=stock_price,
                        )
                        self.virtual_account.stock_long_info.append(position)
                        self.virtual_account.cash_info.available_cash -= diff_value
                        print(f"  买入 {stock_code}: {shares_to_buy:,.0f}股 ({diff_value:,.2f}元)")
                    else:
                        # 需要卖出
                        shares_to_sell = abs(diff_value) / stock_price
                        self._sell_stock(stock_code, shares_to_sell)
                        self.virtual_account.cash_info.available_cash += abs(diff_value)
                        print(
                            f"  卖出 {stock_code}: {shares_to_sell:,.0f}股 ({abs(diff_value):,.2f}元)"
                        )
        else:
            # 非叶子节点递归调仓
            for child in self.children:
                child.rebalance_positions(strategy_allocations)

    def _calculate_total_position_value(self) -> float:
        """计算总持仓价值"""
        total_value = 0
        for position in self.virtual_account.stock_long_info:
            stock_price = self._get_stock_price(position.stock_code)
            total_value += position.stock_amount * stock_price
        return total_value

    def _calculate_current_allocations(self) -> dict[str, float]:
        """计算当前持仓配置"""
        total_value = self._calculate_total_position_value()
        if total_value <= 0:
            return {}

        allocations = {}
        for position in self.virtual_account.stock_long_info:
            stock_price = self._get_stock_price(position.stock_code)
            stock_value = position.stock_amount * stock_price
            allocations[position.stock_code] = stock_value / total_value

        return allocations

    def _sell_stock(self, stock_code: str, shares_to_sell: float) -> None:
        """卖出指定数量的股票"""
        remaining_to_sell = shares_to_sell
        positions_to_remove = []

        for i, position in enumerate(self.virtual_account.stock_long_info):
            if position.stock_code == stock_code and remaining_to_sell > 0:
                if position.stock_amount <= remaining_to_sell:
                    # 全部卖出
                    remaining_to_sell -= position.stock_amount
                    positions_to_remove.append(i)
                else:
                    # 部分卖出
                    position.stock_amount -= remaining_to_sell
                    remaining_to_sell = 0

        # 移除已清仓的持仓
        for i in reversed(positions_to_remove):
            self.virtual_account.stock_long_info.pop(i)

    def get_account_summary(self) -> dict:
        """获取账户摘要 - 只统计根节点和叶子节点，包含期货信息"""
        stock_value = self._calculate_total_position_value()
        cash_value = self.virtual_account.cash_info.available_cash
        pending_value = self.virtual_account.cash_info.pending_purchase_amount

        # 计算期货保证金占用
        futures_margin = 0
        if self.virtual_account.futures_short_info:
            futures_info = self._get_futures_contract_info()
            contract_value = futures_info["current_price"] * futures_info["multiplier"]
            for position in self.virtual_account.futures_short_info:
                position_value = position.futures_amount * contract_value
                futures_margin += position_value * futures_info["margin_rate"]

        # 如果是根节点，需要汇总所有叶子节点的资产
        if self.weight == 1.0 and self.children:
            # 根节点：汇总叶子节点资产
            total_leaf_stock = 0
            total_leaf_cash = 0
            total_leaf_pending = 0
            total_leaf_futures_margin = 0

            def collect_leaf_assets(node):
                nonlocal \
                    total_leaf_stock, \
                    total_leaf_cash, \
                    total_leaf_pending, \
                    total_leaf_futures_margin
                if not node.children:
                    # 叶子节点
                    total_leaf_stock += node._calculate_total_position_value()
                    total_leaf_cash += node.virtual_account.cash_info.available_cash
                    total_leaf_pending += node.virtual_account.cash_info.pending_purchase_amount

                    # 计算期货保证金
                    if node.virtual_account.futures_short_info:
                        futures_info = node._get_futures_contract_info()
                        contract_value = futures_info["current_price"] * futures_info["multiplier"]
                        for position in node.virtual_account.futures_short_info:
                            position_value = position.futures_amount * contract_value
                            total_leaf_futures_margin += (
                                position_value * futures_info["margin_rate"]
                            )
                else:
                    for child in node.children:
                        collect_leaf_assets(child)

            collect_leaf_assets(self)

            total_value = total_leaf_stock + total_leaf_cash + total_leaf_pending

            return {
                "name": self.name,
                "stock_positions": len(self.virtual_account.stock_long_info),
                "stock_value": total_leaf_stock,
                "available_cash": total_leaf_cash,
                "pending_amount": total_leaf_pending,
                "futures_margin": total_leaf_futures_margin,
                "total_value": total_value,
                "is_root": True,
            }
        else:
            # 叶子节点或中间节点
            total_value = stock_value + cash_value + pending_value

            return {
                "name": self.name,
                "stock_positions": len(self.virtual_account.stock_long_info),
                "stock_value": stock_value,
                "available_cash": cash_value,
                "pending_amount": pending_value,
                "futures_margin": futures_margin,
                "total_value": total_value,
                "is_root": False,
            }

    def print_account_details(self, level: int = 0, only_active: bool = True) -> None:
        """
        打印账户详细信息
        only_active: 只显示有资产的节点
        """
        indent = "  " * level
        summary = self.get_account_summary()

        # 如果只显示活跃节点，跳过无资产的中间节点
        if only_active and summary["total_value"] == 0 and self.children:
            for child in self.children:
                child.print_account_details(level, only_active)
            return

        print(f"{indent}📊 {summary['name']}:")
        print(f"{indent}  💼 总资产: {summary['total_value']:,.2f} 元")

        if summary["is_root"]:
            print(f"{indent}  📈 叶子节点股票总价值: {summary['stock_value']:,.2f} 元")
            print(f"{indent}  💰 叶子节点现金总额: {summary['available_cash']:,.2f} 元")
            if summary["futures_margin"] > 0:
                print(f"{indent}  🔥 期货保证金总额: {summary['futures_margin']:,.2f} 元")
        else:
            print(f"{indent}  📈 股票价值: {summary['stock_value']:,.2f} 元")
            print(f"{indent}  💰 可用现金: {summary['available_cash']:,.2f} 元")
            if summary["futures_margin"] > 0:
                print(f"{indent}  🔥 期货保证金: {summary['futures_margin']:,.2f} 元")

        if summary["pending_amount"] != 0:
            if summary["pending_amount"] > 0:
                print(f"{indent}  ⏳ 待申购: {summary['pending_amount']:,.2f} 元")
            else:
                print(f"{indent}  ⏳ 待赎回: {abs(summary['pending_amount']):,.2f} 元")

        if self.virtual_account.stock_long_info and not summary["is_root"]:
            print(f"{indent}  📋 持仓明细:")
            for position in self.virtual_account.stock_long_info:
                value = position.stock_amount * position.stock_cost
                print(
                    f"{indent}    {position.stock_code}: {position.stock_amount:,.0f}股 × {position.stock_cost:.2f}元 = {value:,.2f}元"
                )

        # 递归打印子账户
        if not only_active or not summary["is_root"]:
            for child in self.children:
                child.print_account_details(level + 1, only_active)

    def rebalance_futures_positions(self) -> None:
        """
        期货调仓：根据父节点敞口要求和股票市值调整期货仓位
        """
        if not self.children:
            # 叶子节点 - 如果是期货策略则执行期货调仓
            if self._is_futures_strategy():
                self._rebalance_single_futures()
        else:
            # 非叶子节点 - 递归处理子节点，并协调期货对冲
            for child in self.children:
                child.rebalance_futures_positions()

            # 处理当前节点的期货对冲协调
            self._coordinate_futures_hedging()

    def _is_futures_strategy(self) -> bool:
        """判断是否为期货策略"""
        strategy_type = self.strategy_info.get("strategy_type", "")
        return "期货" in strategy_type or "futures" in strategy_type.lower()

    def _get_futures_contract_info(self) -> dict:
        """获取期货合约信息"""
        contract = self.strategy_info.get("contract", "")

        # 期货合约配置
        futures_configs = {
            "IC期货": {
                "name": "沪深300股指期货",
                "multiplier": 300,  # 每点300元
                "margin_rate": 0.12,  # 12%保证金
                "index_code": "IC",
                "current_price": 4000,  # 模拟当前点位
            },
            "IC500期货": {
                "name": "中证500股指期货",
                "multiplier": 200,  # 每点200元
                "margin_rate": 0.15,  # 15%保证金
                "index_code": "IC500",
                "current_price": 6500,  # 模拟当前点位
            },
            "IM期货": {
                "name": "中证1000股指期货",
                "multiplier": 200,  # 每点200元
                "margin_rate": 0.15,  # 15%保证金
                "index_code": "IM",
                "current_price": 7000,
            },
            "IC/IC500期货": {  # 混合对冲
                "name": "IC/IC500混合期货",
                "multiplier": 250,  # 平均值
                "margin_rate": 0.135,  # 平均值
                "index_code": "mixed",
                "current_price": 5000,
            },
        }

        return futures_configs.get(contract, futures_configs["IC期货"])

    def _get_stock_price(self, stock_code: str) -> float:
        """获取股票价格数据库"""
        stock_prices = {
            # 沪深300成分股
            "000001.SZ": 15.20,  # 平安银行
            "000002.SZ": 8.45,  # 万科A
            "000858.SZ": 185.60,  # 五粮液
            "600519.SH": 1580.00,  # 贵州茅台
            "600036.SH": 42.80,  # 招商银行
            "000066.SZ": 12.30,  # 中国长城
            "600276.SH": 58.90,  # 恒瑞医药
            # 中证500成分股
            "002415.SZ": 28.50,  # 海康威视
            "002594.SZ": 245.80,  # 比亚迪
            "300059.SZ": 13.45,  # 东方财富
            "300750.SZ": 185.20,  # 宁德时代
            "002230.SZ": 45.60,  # 科大讯飞
            "300888.SZ": 125.40,  # 康希诺
            # 中证1000成分股
            "688111.SH": 280.50,  # 金山办公
            "688599.SH": 45.80,  # 天合光能
            "300347.SZ": 58.90,  # 泰格医药
            "300015.SZ": 22.40,  # 爱尔眼科
            "300253.SZ": 18.70,  # 卫宁健康
            "300142.SZ": 35.20,  # 沃森生物
        }

        return stock_prices.get(stock_code, 50.0)  # 默认50元

    def _rebalance_single_futures(self) -> None:
        """单个期货策略调仓"""
        # 获取父节点信息 - 使用动态属性或计算
        parent_target_exposure = getattr(
            self, "_parent_target_exposure", self._get_parent_target_exposure()
        )
        parent_stock_value = getattr(self, "_parent_stock_value", self._get_parent_stock_value())

        if parent_stock_value <= 0:
            print(f"{self.name}: 父节点无股票持仓，期货无需调仓")
            return

        futures_info = self._get_futures_contract_info()

        # 计算目标期货敞口
        # 对于中性策略：target_exposure = 0，期货应完全对冲股票
        # 对于指增策略：target_exposure = 1.0，期货应不对冲
        target_futures_exposure = parent_stock_value * (parent_target_exposure - 1.0)

        # 计算需要的期货手数（负数表示空头）
        contract_value = futures_info["current_price"] * futures_info["multiplier"]
        target_contracts = (
            abs(target_futures_exposure) / contract_value if contract_value > 0 else 0
        )

        # 计算当前期货持仓价值
        current_futures_value = sum(
            pos.futures_amount * pos.futures_cost * futures_info["multiplier"]
            for pos in self.virtual_account.futures_short_info
        )
        current_contracts = current_futures_value / contract_value if contract_value > 0 else 0

        # 计算需要调整的手数
        contracts_diff = target_contracts - current_contracts

        print(f"\n{self.name} 期货调仓:")
        print(f"  期货合约: {futures_info['name']}")
        print(f"  父节点股票市值: {parent_stock_value:,.2f} 元")
        print(f"  父节点目标敞口: {parent_target_exposure:.1f}")
        print(f"  目标期货敞口: {target_futures_exposure:,.2f} 元")
        print(f"  合约价值: {contract_value:,.2f} 元/手")
        print(f"  目标手数: {target_contracts:.1f}手")
        print(f"  当前手数: {current_contracts:.1f}手")

        if abs(contracts_diff) > 0.1:  # 超过0.1手才调仓
            margin_required = abs(contracts_diff) * contract_value * futures_info["margin_rate"]

            if contracts_diff > 0:
                # 增加空头仓位
                if self.virtual_account.cash_info.available_cash >= margin_required:
                    position = FuturesPositionInfo(
                        futures_code=futures_info["index_code"],
                        futures_amount=contracts_diff,
                        futures_cost=futures_info["current_price"],
                    )
                    self.virtual_account.futures_short_info.append(position)
                    self.virtual_account.cash_info.available_cash -= margin_required
                    print(f"  开空 {contracts_diff:.1f}手，保证金: {margin_required:,.2f} 元")
                else:
                    available_cash = self.virtual_account.cash_info.available_cash
                    max_contracts = available_cash / (contract_value * futures_info["margin_rate"])
                    print(
                        f"  现金不足（可用: {available_cash:,.2f}元），只能开空 {max_contracts:.1f}手"
                    )

                    if max_contracts > 0.1:
                        position = FuturesPositionInfo(
                            futures_code=futures_info["index_code"],
                            futures_amount=max_contracts,
                            futures_cost=futures_info["current_price"],
                        )
                        self.virtual_account.futures_short_info.append(position)
                        self.virtual_account.cash_info.available_cash -= (
                            max_contracts * contract_value * futures_info["margin_rate"]
                        )
                        print(f"  实际开空 {max_contracts:.1f}手")
            else:
                # 减少空头仓位
                contracts_to_close = abs(contracts_diff)
                self._close_futures_positions(contracts_to_close, futures_info)
                margin_released = contracts_to_close * contract_value * futures_info["margin_rate"]
                self.virtual_account.cash_info.available_cash += margin_released
                print(f"  平空 {contracts_to_close:.1f}手，释放保证金: {margin_released:,.2f} 元")
        else:
            print(f"  仓位无需调整")

    def _get_parent_target_exposure(self) -> float:
        """获取父节点目标敞口"""
        # 这里需要向上查找父节点，简化起见，根据策略名称判断
        strategy_name = self.name
        if "对冲" in strategy_name:
            return 0.0  # 中性策略目标敞口为0
        elif "指增" in strategy_name:
            return 1.0  # 指增策略目标敞口为1
        else:
            return 0.0  # 默认中性

    def _get_parent_stock_value(self) -> float:
        """获取父节点下所有股票策略的市值总和"""
        # 这是一个简化版本，实际应该通过父节点引用计算
        # 这里使用策略权重估算
        if "300" in self.name:
            return 100000000 * 0.85  # 假设300策略组合85%配置股票
        elif "500" in self.name:
            return 80000000 * 0.85  # 假设500策略组合
        elif "1000" in self.name:
            return 60000000 * 0.85  # 假设1000策略组合
        else:
            return 50000000

    def _close_futures_positions(self, contracts_to_close: float, futures_info: dict) -> None:
        """平仓期货"""
        remaining_to_close = contracts_to_close
        positions_to_remove = []

        for i, position in enumerate(self.virtual_account.futures_short_info):
            if position.futures_code == futures_info["index_code"] and remaining_to_close > 0:
                if position.futures_amount <= remaining_to_close:
                    # 全部平仓
                    remaining_to_close -= position.futures_amount
                    positions_to_remove.append(i)
                else:
                    # 部分平仓
                    position.futures_amount -= remaining_to_close
                    remaining_to_close = 0

        # 移除已平仓的持仓
        for i in reversed(positions_to_remove):
            self.virtual_account.futures_short_info.pop(i)

    def _coordinate_futures_hedging(self) -> None:
        """协调期货对冲 - 在组合级别计算总敞口"""
        target_exposure = self.strategy_info.get("target_exposure")
        if target_exposure is None:
            return

        # 计算子节点总股票市值
        total_stock_value = 0
        futures_children = []

        def collect_stock_value_and_futures(node):
            nonlocal total_stock_value
            if not node.children:
                # 叶子节点
                if node._is_futures_strategy():
                    futures_children.append(node)
                else:
                    total_stock_value += node._calculate_total_position_value()
            else:
                for child in node.children:
                    collect_stock_value_and_futures(child)

        collect_stock_value_and_futures(self)

        if total_stock_value > 0 and futures_children:
            print(f"\n{self.name} 期货协调:")
            print(f"  目标敞口: {target_exposure}")
            print(f"  子节点股票总市值: {total_stock_value:,.2f} 元")
            print(f"  期货策略数: {len(futures_children)}个")

            # 更新期货策略的父节点信息
            for futures_child in futures_children:
                futures_child._parent_stock_value = total_stock_value
                futures_child._parent_target_exposure = target_exposure

    def print_futures_details(self, level: int = 0) -> None:
        """打印期货持仓详情"""
        indent = "  " * level

        if self.virtual_account.futures_short_info:
            print(f"{indent}🔻 期货空头持仓:")
            total_margin = 0
            for position in self.virtual_account.futures_short_info:
                futures_info = self._get_futures_contract_info()
                contract_value = position.futures_cost * futures_info["multiplier"]
                position_value = position.futures_amount * contract_value
                margin = position_value * futures_info["margin_rate"]
                total_margin += margin

                print(
                    f"{indent}    {position.futures_code}: {position.futures_amount:.1f}手 × {contract_value:,.0f}元 "
                    f"= {position_value:,.0f}元 (保证金: {margin:,.0f}元)"
                )

            print(f"{indent}    💰 期货保证金总计: {total_margin:,.2f} 元")

        # 递归打印子节点期货
        for child in self.children:
            if child.virtual_account.futures_short_info or any(
                grandchild.virtual_account.futures_short_info
                for grandchild in self._get_all_descendants()
            ):
                child.print_futures_details(level + 1)

    def _get_all_descendants(self) -> list["StrategyTree"]:
        """获取所有后代节点"""
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child._get_all_descendants())
        return descendants

    def advanced_rebalance(
        self,
        market_signals: dict[str, dict[str, float]],
        trading_system: TradingSystem | None = None,
    ) -> None:
        """
        高级调仓：使用交易系统的完整流程
        market_signals: {"strategy_name": {"stock_code": adjustment, ...}, ...}
        """
        if trading_system is None:
            trading_system = TradingSystem()

        optimizer = TradeOptimizer()

        if not self.children:
            # 叶子节点：执行高级调仓
            if not self._is_futures_strategy() and self.name in market_signals:
                self._execute_advanced_rebalance(
                    market_signals[self.name], optimizer, trading_system
                )
        else:
            # 非叶子节点：收集所有子策略的交易单
            all_orders = []
            strategy_nodes = []

            def collect_strategy_orders(node):
                if not node.children and not node._is_futures_strategy():
                    if node.name in market_signals:
                        signal = market_signals[node.name]
                        target_weights = optimizer.generate_target_weights(node, signal)
                        orders = optimizer.generate_trade_orders(node, target_weights)
                        all_orders.extend(orders)
                        strategy_nodes.append(node)

                        print(f"\n{node.name} 生成交易单:")
                        for order in orders:
                            print(
                                f"  {order.direction.value} {order.stock_code}: {order.target_shares:,.0f}股 "
                                f"({order.target_value:,.2f}元)"
                            )
                else:
                    for child in node.children:
                        collect_strategy_orders(child)

            collect_strategy_orders(self)

            if all_orders:
                print(f"\n{self.name} 产品层汇总:")
                print(f"  收集到 {len(all_orders)} 个交易单")

                # 产品层自成交
                print("\n执行内部自成交...")
                crossed_orders = trading_system.cross_trade(all_orders)

                cross_count = sum(1 for o in crossed_orders if o.executed_shares > 0)
                print(f"  自成交订单数: {cross_count}")

                # 计算总可用现金
                total_cash = sum(
                    node.virtual_account.cash_info.available_cash for node in strategy_nodes
                )

                # 执行剩余订单
                print(f"\n移交外部交易系统执行，可用现金: {total_cash:,.2f} 元")
                remaining_orders = [o for o in crossed_orders if o.remaining_shares > 0.01]

                if remaining_orders:
                    executed_orders, remaining_cash = trading_system.execute_orders(
                        remaining_orders, total_cash
                    )

                    # 统计执行结果
                    total_executed = sum(o.executed_value for o in executed_orders)
                    avg_execution_rate = (
                        sum(o.execution_ratio for o in executed_orders) / len(executed_orders)
                        if executed_orders
                        else 0
                    )

                    print(f"  外部成交金额: {total_executed:,.2f} 元")
                    print(f"  平均成交率: {avg_execution_rate:.1%}")

                    # 应用交易结果到各策略
                    self._apply_trade_results(executed_orders, strategy_nodes)

                    # 处理未成交订单
                    self._handle_unfilled_orders(executed_orders, strategy_nodes)

    def _execute_advanced_rebalance(
        self,
        market_signal: dict[str, float],
        optimizer: TradeOptimizer,
        trading_system: TradingSystem,
    ) -> None:
        """执行单个策略的高级调仓"""
        # 生成目标权重
        target_weights = optimizer.generate_target_weights(self, market_signal)

        # 生成交易单
        orders = optimizer.generate_trade_orders(self, target_weights)

        if not orders:
            print(f"{self.name}: 无需调仓")
            return

        print(f"\n{self.name} 高级调仓:")
        print(f"  目标权重: {target_weights}")

        # 执行交易
        executed_orders, remaining_cash = trading_system.execute_orders(
            orders, self.virtual_account.cash_info.available_cash
        )

        # 应用交易结果
        self._apply_single_strategy_trades(executed_orders)
        self.virtual_account.cash_info.available_cash = remaining_cash

    def _apply_trade_results(
        self, executed_orders: list[TradeOrder], strategy_nodes: list["StrategyTree"]
    ) -> None:
        """应用交易结果到各策略"""
        # 按策略分组订单
        strategy_orders = {}
        for order in executed_orders:
            if order.strategy_name not in strategy_orders:
                strategy_orders[order.strategy_name] = []
            strategy_orders[order.strategy_name].append(order)

        # 应用到各策略
        for strategy_node in strategy_nodes:
            if strategy_node.name in strategy_orders:
                orders = strategy_orders[strategy_node.name]
                strategy_node._apply_single_strategy_trades(orders)

    def _apply_single_strategy_trades(self, orders: list[TradeOrder]) -> None:
        """应用交易结果到单个策略"""
        for order in orders:
            if order.executed_shares <= 0:
                continue

            if order.direction == TradeDirection.BUY:
                # 买入
                position = StockPositionInfo(
                    stock_code=order.stock_code,
                    stock_amount=order.executed_shares,
                    stock_cost=order.price,
                )
                self.virtual_account.stock_long_info.append(position)
                self.virtual_account.cash_info.available_cash -= order.executed_value

            elif order.direction == TradeDirection.SELL:
                # 卖出
                self._sell_stock(order.stock_code, order.executed_shares)
                self.virtual_account.cash_info.available_cash += order.executed_value

    def _handle_unfilled_orders(
        self, executed_orders: list[TradeOrder], strategy_nodes: list["StrategyTree"]
    ) -> None:
        """处理未成交订单"""
        unfilled_orders = [o for o in executed_orders if o.remaining_shares > 0.01]

        if not unfilled_orders:
            return

        print(f"\n处理未成交订单 ({len(unfilled_orders)}个):")

        # 按股票代码分组未成交订单
        unfilled_by_stock = {}
        for order in unfilled_orders:
            if order.stock_code not in unfilled_by_stock:
                unfilled_by_stock[order.stock_code] = {"buy": [], "sell": []}

            if order.direction == TradeDirection.BUY:
                unfilled_by_stock[order.stock_code]["buy"].append(order)
            else:
                unfilled_by_stock[order.stock_code]["sell"].append(order)

        # 按权重分配未成交部分
        for stock_code, orders_dict in unfilled_by_stock.items():
            buy_orders = orders_dict["buy"]
            sell_orders = orders_dict["sell"]

            if buy_orders:
                total_unfilled_buy = sum(o.remaining_shares for o in buy_orders)
                total_target_buy = sum(o.target_shares for o in buy_orders)

                if total_target_buy > 0:
                    for order in buy_orders:
                        weight = order.target_shares / total_target_buy
                        allocated_unfilled = total_unfilled_buy * weight
                        print(
                            f"  {order.strategy_name} {stock_code} 未买入: {allocated_unfilled:,.0f}股"
                        )

            if sell_orders:
                total_unfilled_sell = sum(o.remaining_shares for o in sell_orders)
                total_target_sell = sum(o.target_shares for o in sell_orders)

                if total_target_sell > 0:
                    for order in sell_orders:
                        weight = order.target_shares / total_target_sell
                        allocated_unfilled = total_unfilled_sell * weight
                        print(
                            f"  {order.strategy_name} {stock_code} 未卖出: {allocated_unfilled:,.0f}股"
                        )
