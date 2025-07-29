from src.entity.strategy import CashInfo, StrategyTree, VirtualAccount


def create_comprehensive_strategy_tree():
    """
    创建一个完整的策略树结构，每层权重和为1
    根节点：基金总持仓
    ├── 中性策略 (60%)
    │   ├── 300对冲 (40%)
    │   │   ├── 300基准策略组合（85%）
    │   │   │   ├── mars_v8（47%）
    │   │   │   └── rossa_v5（53%）
    │   │   └── 300期货对冲（15%）
    │   ├── 500对冲 (35%)
    │   │   ├── 500基准策略组合（85%）
    │   │   │   ├── titan_v2（60%）
    │   │   │   └── apollo_v3（40%）
    │   │   └── 500期货对冲（15%）
    │   └── 1000对冲 (25%)
    │       ├── 1000基准策略组合（85%）
    │       │   ├── cosmos_v4（45%）
    │       │   └── jupiter_v6（55%）
    │       └── 1000期货对冲（15%）
    └── 指增策略 (40%)
        └── 300指增 (100%)
            ├── 300指增基准策略组合（97%）
            │   ├── mars_v8（42%）
            │   └── rossa_v5（58%）
            └── 300指增期货（3%）
    """

    # 叶子节点策略 - 300基准策略 (权重和为1.0)
    mars_v8_300 = StrategyTree(
        fund_id=75,
        weight=0.47,  # 修正：47%
        name="mars_v8_300",
        children=[],
        virtual_account=VirtualAccount(),
        strategy_info={"strategy_type": "基准策略", "universe": "沪深300", "model": "mars_v8"},
    )

    rossa_v5_300 = StrategyTree(
        fund_id=75,
        weight=0.53,  # 修正：53%，总计100%
        name="rossa_v5_300",
        children=[],
        virtual_account=VirtualAccount(),
        strategy_info={"strategy_type": "基准策略", "universe": "沪深300", "model": "rossa_v5"},
    )

    # 叶子节点策略 - 500基准策略 (权重和为1.0)
    titan_v2_500 = StrategyTree(
        fund_id=75,
        weight=0.60,  # 修正：60%
        name="titan_v2_500",
        children=[],
        virtual_account=VirtualAccount(),
        strategy_info={"strategy_type": "基准策略", "universe": "中证500", "model": "titan_v2"},
    )

    apollo_v3_500 = StrategyTree(
        fund_id=75,
        weight=0.40,  # 修正：40%，总计100%
        name="apollo_v3_500",
        children=[],
        virtual_account=VirtualAccount(),
        strategy_info={"strategy_type": "基准策略", "universe": "中证500", "model": "apollo_v3"},
    )

    # 叶子节点策略 - 1000基准策略 (权重和为1.0)
    cosmos_v4_1000 = StrategyTree(
        fund_id=75,
        weight=0.45,  # 修正：45%
        name="cosmos_v4_1000",
        children=[],
        virtual_account=VirtualAccount(),
        strategy_info={"strategy_type": "基准策略", "universe": "中证1000", "model": "cosmos_v4"},
    )

    jupiter_v6_1000 = StrategyTree(
        fund_id=75,
        weight=0.55,  # 修正：55%，总计100%
        name="jupiter_v6_1000",
        children=[],
        virtual_account=VirtualAccount(),
        strategy_info={"strategy_type": "基准策略", "universe": "中证1000", "model": "jupiter_v6"},
    )

    # 期货策略
    futures_300_hedge = StrategyTree(
        fund_id=75,
        weight=0.15,
        name="期货300对冲",
        children=[],
        virtual_account=VirtualAccount(),
        strategy_info={"strategy_type": "期货对冲", "contract": "IC期货", "purpose": "对冲300敞口"},
    )

    futures_500_hedge = StrategyTree(
        fund_id=75,
        weight=0.15,
        name="期货500对冲",
        children=[],
        virtual_account=VirtualAccount(),
        strategy_info={
            "strategy_type": "期货对冲",
            "contract": "IC/IH期货",
            "purpose": "对冲500敞口",
        },
    )

    futures_1000_hedge = StrategyTree(
        fund_id=75,
        weight=0.15,
        name="期货1000对冲",
        children=[],
        virtual_account=VirtualAccount(),
        strategy_info={
            "strategy_type": "期货对冲",
            "contract": "IM期货",
            "purpose": "对冲1000敞口",
        },
    )

    futures_300_enhancement = StrategyTree(
        fund_id=75,
        weight=0.03,
        name="期货300指增",
        children=[],
        virtual_account=VirtualAccount(),
        strategy_info={
            "strategy_type": "期货指增",
            "contract": "IC期货",
            "purpose": "指数增强敞口管理",
        },
    )

    # 指增的300基准策略（权重和为1.0）
    mars_v8_300_enhancement = StrategyTree(
        fund_id=75,
        weight=0.42,  # 修正：42%
        name="mars_v8_300_指增",
        children=[],
        virtual_account=VirtualAccount(),
        strategy_info={
            "strategy_type": "基准策略",
            "universe": "沪深300",
            "model": "mars_v8",
            "purpose": "指数增强",
        },
    )

    rossa_v5_300_enhancement = StrategyTree(
        fund_id=75,
        weight=0.58,  # 修正：58%，总计100%
        name="rossa_v5_300_指增",
        children=[],
        virtual_account=VirtualAccount(),
        strategy_info={
            "strategy_type": "基准策略",
            "universe": "沪深300",
            "model": "rossa_v5",
            "purpose": "指数增强",
        },
    )

    # 基准策略组合
    benchmark_300_combo = StrategyTree(
        fund_id=75,
        weight=0.85,
        name="300基准策略组合",
        children=[mars_v8_300, rossa_v5_300],
        virtual_account=VirtualAccount(),
        strategy_info={"strategy_type": "基准策略组合", "universe": "沪深300"},
    )

    benchmark_500_combo = StrategyTree(
        fund_id=75,
        weight=0.85,
        name="500基准策略组合",
        children=[titan_v2_500, apollo_v3_500],
        virtual_account=VirtualAccount(),
        strategy_info={"strategy_type": "基准策略组合", "universe": "中证500"},
    )

    benchmark_1000_combo = StrategyTree(
        fund_id=75,
        weight=0.85,
        name="1000基准策略组合",
        children=[cosmos_v4_1000, jupiter_v6_1000],
        virtual_account=VirtualAccount(),
        strategy_info={"strategy_type": "基准策略组合", "universe": "中证1000"},
    )

    benchmark_300_enhancement_combo = StrategyTree(
        fund_id=75,
        weight=0.97,
        name="300指增基准策略组合",
        children=[mars_v8_300_enhancement, rossa_v5_300_enhancement],
        virtual_account=VirtualAccount(),
        strategy_info={
            "strategy_type": "基准策略组合",
            "universe": "沪深300",
            "purpose": "指数增强",
        },
    )

    # 对冲策略 (权重和为1.0: 0.4 + 0.35 + 0.25 = 1.0)
    hedge_300 = StrategyTree(
        fund_id=75,
        weight=0.40,  # 修正：40%
        name="300对冲",
        children=[benchmark_300_combo, futures_300_hedge],
        virtual_account=VirtualAccount(cash_info=CashInfo(available_cash=50000000)),
        strategy_info={
            "strategy_type": "中性对冲策略",
            "universe": "沪深300",
            "target_exposure": 0,
        },
    )

    hedge_500 = StrategyTree(
        fund_id=75,
        weight=0.35,  # 35%
        name="500对冲",
        children=[benchmark_500_combo, futures_500_hedge],
        virtual_account=VirtualAccount(cash_info=CashInfo(available_cash=30000000)),
        strategy_info={
            "strategy_type": "中性对冲策略",
            "universe": "中证500",
            "target_exposure": 0,
        },
    )

    hedge_1000 = StrategyTree(
        fund_id=75,
        weight=0.25,  # 修正：25%，总计100%
        name="1000对冲",
        children=[benchmark_1000_combo, futures_1000_hedge],
        virtual_account=VirtualAccount(cash_info=CashInfo(available_cash=20000000)),
        strategy_info={
            "strategy_type": "中性对冲策略",
            "universe": "中证1000",
            "target_exposure": 0,
        },
    )

    # 指增策略
    enhancement_300 = StrategyTree(
        fund_id=75,
        weight=1.0,  # 指增策略下只有一个子策略，权重为100%
        name="300指增",
        children=[benchmark_300_enhancement_combo, futures_300_enhancement],
        virtual_account=VirtualAccount(cash_info=CashInfo(available_cash=40000000)),
        strategy_info={
            "strategy_type": "指数增强策略",
            "universe": "沪深300",
            "target_exposure": 1.0,
            "benchmark": "沪深300指数",
        },
    )

    # 大策略类 (权重和为1.0: 0.6 + 0.4 = 1.0)
    neutral_strategy = StrategyTree(
        fund_id=75,
        weight=0.60,  # 60%
        name="中性策略",
        children=[hedge_300, hedge_500, hedge_1000],
        virtual_account=VirtualAccount(cash_info=CashInfo(available_cash=100000000)),
        strategy_info={
            "strategy_type": "市场中性策略",
            "target_exposure": 0,
            "description": "通过多空配置实现市场中性",
        },
    )

    enhancement_strategy = StrategyTree(
        fund_id=75,
        weight=0.40,  # 40%，总计100%
        name="指增策略",
        children=[enhancement_300],
        virtual_account=VirtualAccount(cash_info=CashInfo(available_cash=60000000)),
        strategy_info={
            "strategy_type": "指数增强策略",
            "target_exposure": 1.0,
            "description": "通过alpha策略实现指数增强",
        },
    )

    # 根节点
    root_strategy = StrategyTree(
        fund_id=75,
        weight=1.0,
        name="综合量化基金",
        children=[neutral_strategy, enhancement_strategy],
        virtual_account=VirtualAccount(cash_info=CashInfo(available_cash=200000000)),
        strategy_info={
            "fund_type": "量化多策略基金",
            "total_aum": 2000000000,
            "inception_date": "2024-01-01",
            "description": "综合中性策略和指增策略的量化基金",
        },
    )

    return root_strategy


def print_strategy_tree(strategy: StrategyTree, level: int = 0) -> None:
    """打印策略树结构"""
    indent = "  " * level
    print(f"{indent}├─ {strategy.name} (权重: {strategy.weight:.1%})")

    # 打印虚拟账户信息（如果有现金）
    if strategy.virtual_account.cash_info.available_cash > 0:
        cash_amount = strategy.virtual_account.cash_info.available_cash
        print(f"{indent}   💰 可用现金: {cash_amount:,} 元")

    if strategy.virtual_account.cash_info.pending_purchase_amount != 0:
        pending_amount = strategy.virtual_account.cash_info.pending_purchase_amount
        if pending_amount > 0:
            print(f"{indent}   📈 待申购金额: {pending_amount:,} 元")
        else:
            print(f"{indent}   📉 待赎回金额: {abs(pending_amount):,} 元")

    # 打印策略信息
    if strategy.strategy_info:
        strategy_type = strategy.strategy_info.get("strategy_type", "")
        if strategy_type:
            print(f"{indent}   📊 类型: {strategy_type}")

        universe = strategy.strategy_info.get("universe", "")
        if universe:
            print(f"{indent}   🎯 标的: {universe}")

        model = strategy.strategy_info.get("model", "")
        if model:
            print(f"{indent}   🤖 模型: {model}")

    # 递归打印子策略
    for child in strategy.children:
        print_strategy_tree(child, level + 1)


def validate_strategy_tree_weights(strategy: StrategyTree, level: int = 0) -> bool:
    """验证策略树的权重分配是否正确"""
    indent = "  " * level
    is_valid = True

    if strategy.children:
        total_weight = sum(child.weight for child in strategy.children)
        print(f"{indent}{strategy.name}: 子节点权重和 = {total_weight:.3f}")

        if abs(total_weight - 1.0) > 1e-6:
            print(f"{indent}❌ 权重和不为1！")
            is_valid = False
        else:
            print(f"{indent}✅ 权重和正确")

        # 递归验证子节点
        for child in strategy.children:
            child_valid = validate_strategy_tree_weights(child, level + 1)
            is_valid = is_valid and child_valid

    return is_valid


def test_pending_amount_allocation():
    """测试待申购金额分配功能"""
    print("\n测试待申购金额分配功能：")
    print("=" * 60)

    strategy_tree = create_comprehensive_strategy_tree()

    # 分配1000万待申购金额
    allocation_amount = 10000000
    print(f"分配 {allocation_amount:,} 元待申购金额...")

    strategy_tree.allocate_pending_amount(allocation_amount)

    def print_pending_amounts(strategy: StrategyTree, level: int = 0):
        indent = "  " * level
        pending = strategy.virtual_account.cash_info.pending_purchase_amount
        if pending != 0:
            print(f"{indent}{strategy.name}: {pending:,.2f} 元")

        for child in strategy.children:
            print_pending_amounts(child, level + 1)

    print("\n各策略待申购金额分配结果：")
    print_pending_amounts(strategy_tree)


if __name__ == "__main__":
    print("生成综合策略树...")
    strategy_tree = create_comprehensive_strategy_tree()

    print("\n验证权重分配：")
    print("=" * 60)
    is_valid = validate_strategy_tree_weights(strategy_tree)
    print(f"\n整体权重验证结果: {'✅ 通过' if is_valid else '❌ 失败'}")

    print("\n策略树结构：")
    print("=" * 60)
    print_strategy_tree(strategy_tree)

    print("\n\n策略统计信息：")
    print("=" * 60)

    def collect_strategies(
        strategy: StrategyTree, strategies: list[StrategyTree] | None = None
    ) -> list[StrategyTree]:
        if strategies is None:
            strategies = []
        strategies.append(strategy)
        for child in strategy.children:
            collect_strategies(child, strategies)
        return strategies

    all_strategies = collect_strategies(strategy_tree)

    print(f"总策略数量: {len(all_strategies)}")
    print(f"叶子策略数量: {len([s for s in all_strategies if not s.children])}")
    print(f"组合策略数量: {len([s for s in all_strategies if s.children])}")

    # 按策略类型统计
    strategy_types = {}
    for strategy in all_strategies:
        strategy_type = strategy.strategy_info.get("strategy_type", "未分类")
        strategy_types[strategy_type] = strategy_types.get(strategy_type, 0) + 1

    print("\n策略类型分布：")
    for strategy_type, count in strategy_types.items():
        print(f"  {strategy_type}: {count}个")

    # 使用内置的权重验证方法
    print("\n\n使用内置验证方法：")
    print("=" * 60)
    try:
        strategy_tree.validate_weights()
        print("✅ 内置权重验证通过")
    except ValueError as e:
        print(f"❌ 内置权重验证失败: {e}")

    # 测试待申购金额分配
    test_pending_amount_allocation()
