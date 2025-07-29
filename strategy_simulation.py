from src.entity.strategy import CashInfo, StrategyTree, VirtualAccount


def create_simple_strategy_tree():
    """
    创建一个简化的策略树用于模拟

    量化基金
    ├── 股票策略 (70%)
    │   ├── 沪深300策略 (60%)
    │   └── 中证500策略 (40%)
    └── 现金管理 (30%)
    """

    # 叶子节点 - 具体策略
    hs300_strategy = StrategyTree(
        fund_id=1,
        weight=0.60,
        name="沪深300策略",
        children=[],
        virtual_account=VirtualAccount(cash_info=CashInfo()),
        strategy_info={"strategy_type": "股票多头", "universe": "沪深300"},
    )

    zz500_strategy = StrategyTree(
        fund_id=2,
        weight=0.40,
        name="中证500策略",
        children=[],
        virtual_account=VirtualAccount(cash_info=CashInfo()),
        strategy_info={"strategy_type": "股票多头", "universe": "中证500"},
    )

    cash_management = StrategyTree(
        fund_id=3,
        weight=0.30,
        name="现金管理",
        children=[],
        virtual_account=VirtualAccount(cash_info=CashInfo()),
        strategy_info={"strategy_type": "现金管理", "universe": "货币基金"},
    )

    # 中间节点 - 股票策略组合
    stock_strategy = StrategyTree(
        fund_id=4,
        weight=0.70,
        name="股票策略",
        children=[hs300_strategy, zz500_strategy],
        virtual_account=VirtualAccount(cash_info=CashInfo()),
        strategy_info={"strategy_type": "股票组合"},
    )

    # 根节点
    root_strategy = StrategyTree(
        fund_id=5,
        weight=1.0,
        name="量化基金",
        children=[stock_strategy, cash_management],
        virtual_account=VirtualAccount(cash_info=CashInfo()),
        strategy_info={"fund_type": "量化多策略基金"},
    )

    return root_strategy


def simulate_fund_operations():
    """模拟基金运作过程"""

    print("🚀 创建策略树（初始状态：所有账户为0）")
    print("=" * 60)

    fund = create_simple_strategy_tree()

    print("初始账户状态:")
    fund.print_account_details()

    print("\n" + "=" * 60)
    print("📈 第一步：申购操作")
    print("=" * 60)

    # 模拟申购1000万
    subscription_amount = 10000000
    print(f"客户申购: {subscription_amount:,.2f} 元")
    fund.process_subscription(subscription_amount)

    print("\n申购后账户状态:")
    fund.print_account_details()

    print("\n" + "=" * 60)
    print("🏗️ 第二步：建仓操作")
    print("=" * 60)

    # 为沪深300策略分配股票
    hs300_allocations = {
        "000001.SZ": 0.3,  # 平安银行 30%
        "000002.SZ": 0.3,  # 万科A 30%
        "000858.SZ": 0.4,  # 五粮液 40%
    }

    # 为中证500策略分配股票
    zz500_allocations = {
        "002415.SZ": 0.5,  # 海康威视 50%
        "002594.SZ": 0.3,  # 比亚迪 30%
        "300059.SZ": 0.2,  # 东方财富 20%
    }

    print("为沪深300策略建仓:")
    fund.children[0].children[0].build_positions_from_pending(hs300_allocations)

    print("\n为中证500策略建仓:")
    fund.children[0].children[1].build_positions_from_pending(zz500_allocations)

    print("\n为现金管理策略建仓:")
    fund.children[1].build_positions_from_pending()  # 转为现金

    print("\n建仓后账户状态:")
    fund.print_account_details()

    print("\n" + "=" * 60)
    print("🔄 第三步：调仓操作")
    print("=" * 60)

    # 模拟市场变化后的调仓
    print("模拟策略信号变化，需要调整持仓...")

    # 沪深300策略调仓 - 减持万科，增持平安银行
    new_hs300_allocations = {
        "000001.SZ": 0.5,  # 平安银行 30% -> 50%
        "000002.SZ": 0.1,  # 万科A 30% -> 10%
        "000858.SZ": 0.4,  # 五粮液 40% -> 40%
    }

    fund.children[0].children[0].rebalance_positions(new_hs300_allocations)

    # 中证500策略调仓 - 新增股票
    new_zz500_allocations = {
        "002415.SZ": 0.3,  # 海康威视 50% -> 30%
        "002594.SZ": 0.4,  # 比亚迪 30% -> 40%
        "300059.SZ": 0.1,  # 东方财富 20% -> 10%
        "300750.SZ": 0.2,  # 宁德时代 新增 20%
    }

    fund.children[0].children[1].rebalance_positions(new_zz500_allocations)

    print("\n调仓后账户状态:")
    fund.print_account_details()

    print("\n" + "=" * 60)
    print("💰 第四步：新申购 + 再次调仓")
    print("=" * 60)

    # 新申购500万
    new_subscription = 5000000
    print(f"新申购: {new_subscription:,.2f} 元")
    fund.process_subscription(new_subscription)

    # 建仓新申购资金
    print("\n为新申购资金建仓:")
    fund.children[0].children[0].build_positions_from_pending(new_hs300_allocations)
    fund.children[0].children[1].build_positions_from_pending(new_zz500_allocations)
    fund.children[1].build_positions_from_pending()

    print("\n新申购建仓后账户状态:")
    fund.print_account_details()

    print("\n" + "=" * 60)
    print("📊 最终统计")
    print("=" * 60)

    # 统计各策略最终状态 - 只统计叶子节点和根节点，避免重复
    def get_leaf_and_root_summary(
        strategy: StrategyTree, summaries: list | None = None, is_root: bool = True
    ):
        if summaries is None:
            summaries = []

        # 根节点总是包含
        if is_root:
            summary = strategy.get_account_summary()
            summaries.append(("根节点", summary))

        # 如果是叶子节点，也包含
        if not strategy.children:
            summary = strategy.get_account_summary()
            summaries.append(("叶子节点", summary))

        # 递归处理子节点
        for child in strategy.children:
            get_leaf_and_root_summary(child, summaries, False)

        return summaries

    all_summaries = get_leaf_and_root_summary(fund)

    print("各策略资产汇总（避免重复统计）:")
    leaf_total = 0
    root_total = 0

    for node_type, summary in all_summaries:
        print(
            f"  [{node_type}] {summary['name']:15} | 总资产: {summary['total_value']:>12,.2f} 元 | 持仓数: {summary['stock_positions']}"
        )
        if node_type == "叶子节点":
            leaf_total += summary["total_value"]
        elif node_type == "根节点":
            root_total = summary["total_value"]

    print(f"\n💎 根节点总资产: {root_total:,.2f} 元")
    print(f"💎 叶子节点资产合计: {leaf_total:,.2f} 元")
    print(f"📈 申购总额: {subscription_amount + new_subscription:,.2f} 元")
    print(
        f"📊 根节点资产匹配: {'✅ 正确' if abs(root_total - (subscription_amount + new_subscription)) < 0.01 else '❌ 异常'}"
    )
    print(
        f"📊 叶子节点资产匹配: {'✅ 正确' if abs(leaf_total - (subscription_amount + new_subscription)) < 0.01 else '❌ 异常'}"
    )


def test_weight_validation():
    """测试权重验证"""
    print("\n" + "=" * 60)
    print("🔍 权重验证测试")
    print("=" * 60)

    fund = create_simple_strategy_tree()

    try:
        fund.validate_weights()
        print("✅ 权重验证通过")
    except ValueError as e:
        print(f"❌ 权重验证失败: {e}")


if __name__ == "__main__":
    print("🎯 策略树模拟系统")
    print("=" * 60)

    # 运行模拟
    simulate_fund_operations()

    # 验证权重
    test_weight_validation()

    print("\n✨ 模拟完成！")
