from src.entity.strategy import CashInfo, StrategyTree, VirtualAccount


def create_advanced_strategy_tree():
    """
    创建高级策略树，参照复杂的量化基金配置
    只有根节点和叶子节点有账户信息

    综合量化基金
    ├── 中性策略 (60%)
    │   ├── 300对冲 (40%)
    │   │   ├── 300基准策略组合 (85%)
    │   │   │   ├── mars_v8_300 (47%)
    │   │   │   └── rossa_v5_300 (53%)
    │   │   └── 期货300对冲 (15%)
    │   ├── 500对冲 (35%)
    │   │   ├── 500基准策略组合 (85%)
    │   │   │   ├── titan_v2_500 (60%)
    │   │   │   └── apollo_v3_500 (40%)
    │   │   └── 期货500对冲 (15%)
    │   └── 1000对冲 (25%)
    │       ├── 1000基准策略组合 (85%)
    │       │   ├── cosmos_v4_1000 (45%)
    │       │   └── jupiter_v6_1000 (55%)
    │       └── 期货1000对冲 (15%)
    └── 指增策略 (40%)
        └── 300指增 (100%)
            ├── 300指增基准策略组合 (97%)
            │   ├── mars_v8_300_指增 (42%)
            │   └── rossa_v5_300_指增 (58%)
            └── 期货300指增 (3%)
    """

    # ==================== 叶子节点策略 ====================

    # 沪深300基准策略叶子节点
    mars_v8_300 = StrategyTree(
        fund_id=1,
        weight=0.47,
        name="mars_v8_300",
        children=[],
        virtual_account=VirtualAccount(cash_info=CashInfo()),
        strategy_info={"strategy_type": "基准策略", "universe": "沪深300", "model": "mars_v8"},
    )

    rossa_v5_300 = StrategyTree(
        fund_id=2,
        weight=0.53,
        name="rossa_v5_300",
        children=[],
        virtual_account=VirtualAccount(cash_info=CashInfo()),
        strategy_info={"strategy_type": "基准策略", "universe": "沪深300", "model": "rossa_v5"},
    )

    # 中证500基准策略叶子节点
    titan_v2_500 = StrategyTree(
        fund_id=3,
        weight=0.60,
        name="titan_v2_500",
        children=[],
        virtual_account=VirtualAccount(cash_info=CashInfo()),
        strategy_info={"strategy_type": "基准策略", "universe": "中证500", "model": "titan_v2"},
    )

    apollo_v3_500 = StrategyTree(
        fund_id=4,
        weight=0.40,
        name="apollo_v3_500",
        children=[],
        virtual_account=VirtualAccount(cash_info=CashInfo()),
        strategy_info={"strategy_type": "基准策略", "universe": "中证500", "model": "apollo_v3"},
    )

    # 中证1000基准策略叶子节点
    cosmos_v4_1000 = StrategyTree(
        fund_id=5,
        weight=0.45,
        name="cosmos_v4_1000",
        children=[],
        virtual_account=VirtualAccount(cash_info=CashInfo()),
        strategy_info={"strategy_type": "基准策略", "universe": "中证1000", "model": "cosmos_v4"},
    )

    jupiter_v6_1000 = StrategyTree(
        fund_id=6,
        weight=0.55,
        name="jupiter_v6_1000",
        children=[],
        virtual_account=VirtualAccount(cash_info=CashInfo()),
        strategy_info={"strategy_type": "基准策略", "universe": "中证1000", "model": "jupiter_v6"},
    )

    # 期货策略叶子节点（初始无现金）
    futures_300_hedge = StrategyTree(
        fund_id=7,
        weight=0.15,
        name="期货300对冲",
        children=[],
        virtual_account=VirtualAccount(cash_info=CashInfo()),  # 初始无现金
        strategy_info={"strategy_type": "期货对冲", "contract": "IC期货", "purpose": "对冲300敞口"},
    )

    futures_500_hedge = StrategyTree(
        fund_id=8,
        weight=0.15,
        name="期货500对冲",
        children=[],
        virtual_account=VirtualAccount(cash_info=CashInfo()),  # 初始无现金
        strategy_info={
            "strategy_type": "期货对冲",
            "contract": "IC500期货",
            "purpose": "对冲500敞口",
        },
    )

    futures_1000_hedge = StrategyTree(
        fund_id=9,
        weight=0.15,
        name="期货1000对冲",
        children=[],
        virtual_account=VirtualAccount(cash_info=CashInfo()),  # 初始无现金
        strategy_info={
            "strategy_type": "期货对冲",
            "contract": "IM期货",
            "purpose": "对冲1000敞口",
        },
    )

    # 指增策略叶子节点
    mars_v8_300_enhancement = StrategyTree(
        fund_id=10,
        weight=0.42,
        name="mars_v8_300_指增",
        children=[],
        virtual_account=VirtualAccount(cash_info=CashInfo()),
        strategy_info={
            "strategy_type": "基准策略",
            "universe": "沪深300",
            "model": "mars_v8",
            "purpose": "指数增强",
        },
    )

    rossa_v5_300_enhancement = StrategyTree(
        fund_id=11,
        weight=0.58,
        name="rossa_v5_300_指增",
        children=[],
        virtual_account=VirtualAccount(cash_info=CashInfo()),
        strategy_info={
            "strategy_type": "基准策略",
            "universe": "沪深300",
            "model": "rossa_v5",
            "purpose": "指数增强",
        },
    )

    futures_300_enhancement = StrategyTree(
        fund_id=12,
        weight=0.03,
        name="期货300指增",
        children=[],
        virtual_account=VirtualAccount(cash_info=CashInfo()),  # 初始无现金
        strategy_info={
            "strategy_type": "期货指增",
            "contract": "IC期货",
            "purpose": "指数增强敞口管理",
        },
    )

    # ==================== 中间节点（无账户信息）====================

    # 基准策略组合
    benchmark_300_combo = StrategyTree(
        fund_id=100,
        weight=0.85,
        name="300基准策略组合",
        children=[mars_v8_300, rossa_v5_300],
        virtual_account=VirtualAccount(),  # 中间节点无账户信息
        strategy_info={"strategy_type": "基准策略组合", "universe": "沪深300"},
    )

    benchmark_500_combo = StrategyTree(
        fund_id=101,
        weight=0.85,
        name="500基准策略组合",
        children=[titan_v2_500, apollo_v3_500],
        virtual_account=VirtualAccount(),
        strategy_info={"strategy_type": "基准策略组合", "universe": "中证500"},
    )

    benchmark_1000_combo = StrategyTree(
        fund_id=102,
        weight=0.85,
        name="1000基准策略组合",
        children=[cosmos_v4_1000, jupiter_v6_1000],
        virtual_account=VirtualAccount(),
        strategy_info={"strategy_type": "基准策略组合", "universe": "中证1000"},
    )

    benchmark_300_enhancement_combo = StrategyTree(
        fund_id=103,
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

    # 对冲策略
    hedge_300 = StrategyTree(
        fund_id=200,
        weight=0.40,
        name="300对冲",
        children=[benchmark_300_combo, futures_300_hedge],
        virtual_account=VirtualAccount(),
        strategy_info={
            "strategy_type": "中性对冲策略",
            "universe": "沪深300",
            "target_exposure": 0,
        },
    )

    hedge_500 = StrategyTree(
        fund_id=201,
        weight=0.35,
        name="500对冲",
        children=[benchmark_500_combo, futures_500_hedge],
        virtual_account=VirtualAccount(),
        strategy_info={
            "strategy_type": "中性对冲策略",
            "universe": "中证500",
            "target_exposure": 0,
        },
    )

    hedge_1000 = StrategyTree(
        fund_id=202,
        weight=0.25,
        name="1000对冲",
        children=[benchmark_1000_combo, futures_1000_hedge],
        virtual_account=VirtualAccount(),
        strategy_info={
            "strategy_type": "中性对冲策略",
            "universe": "中证1000",
            "target_exposure": 0,
        },
    )

    # 指增策略
    enhancement_300 = StrategyTree(
        fund_id=300,
        weight=1.0,
        name="300指增",
        children=[benchmark_300_enhancement_combo, futures_300_enhancement],
        virtual_account=VirtualAccount(),
        strategy_info={
            "strategy_type": "指数增强策略",
            "universe": "沪深300",
            "target_exposure": 1.0,
        },
    )

    # 大策略类
    neutral_strategy = StrategyTree(
        fund_id=400,
        weight=0.60,
        name="中性策略",
        children=[hedge_300, hedge_500, hedge_1000],
        virtual_account=VirtualAccount(),
        strategy_info={"strategy_type": "市场中性策略", "target_exposure": 0},
    )

    enhancement_strategy = StrategyTree(
        fund_id=401,
        weight=0.40,
        name="指增策略",
        children=[enhancement_300],
        virtual_account=VirtualAccount(),
        strategy_info={"strategy_type": "指数增强策略", "target_exposure": 1.0},
    )

    # ==================== 根节点（有账户信息）====================

    root_strategy = StrategyTree(
        fund_id=500,
        weight=1.0,
        name="综合量化基金",
        children=[neutral_strategy, enhancement_strategy],
        virtual_account=VirtualAccount(cash_info=CashInfo()),  # 根节点有账户信息
        strategy_info={
            "fund_type": "量化多策略基金",
            "total_aum": 2000000000,
            "inception_date": "2024-01-01",
            "description": "综合中性策略和指增策略的量化基金",
        },
    )

    return root_strategy


def get_strategy_allocations():
    """
    定义各策略的股票配置
    """
    return {
        # 沪深300策略配置
        "mars_v8_300": {
            "000001.SZ": 0.15,  # 平安银行
            "000002.SZ": 0.12,  # 万科A
            "000858.SZ": 0.18,  # 五粮液
            "600519.SH": 0.20,  # 贵州茅台
            "600036.SH": 0.15,  # 招商银行
            "000066.SZ": 0.20,  # 中国长城
        },
        "rossa_v5_300": {
            "600519.SH": 0.25,  # 贵州茅台
            "000858.SZ": 0.20,  # 五粮液
            "600036.SH": 0.18,  # 招商银行
            "000001.SZ": 0.12,  # 平安银行
            "600276.SH": 0.15,  # 恒瑞医药
            "000002.SZ": 0.10,  # 万科A
        },
        # 中证500策略配置
        "titan_v2_500": {
            "002415.SZ": 0.25,  # 海康威视
            "002594.SZ": 0.20,  # 比亚迪
            "300059.SZ": 0.15,  # 东方财富
            "300750.SZ": 0.20,  # 宁德时代
            "002230.SZ": 0.12,  # 科大讯飞
            "300888.SZ": 0.08,  # 康希诺
        },
        "apollo_v3_500": {
            "300750.SZ": 0.30,  # 宁德时代
            "002594.SZ": 0.25,  # 比亚迪
            "002415.SZ": 0.15,  # 海康威视
            "300059.SZ": 0.12,  # 东方财富
            "002230.SZ": 0.10,  # 科大讯飞
            "300888.SZ": 0.08,  # 康希诺
        },
        # 中证1000策略配置
        "cosmos_v4_1000": {
            "688111.SH": 0.20,  # 金山办公
            "688599.SH": 0.18,  # 天合光能
            "300347.SZ": 0.15,  # 泰格医药
            "300015.SZ": 0.12,  # 爱尔眼科
            "300253.SZ": 0.15,  # 卫宁健康
            "300142.SZ": 0.20,  # 沃森生物
        },
        "jupiter_v6_1000": {
            "300142.SZ": 0.25,  # 沃森生物
            "688111.SH": 0.20,  # 金山办公
            "300015.SZ": 0.18,  # 爱尔眼科
            "300347.SZ": 0.15,  # 泰格医药
            "688599.SH": 0.12,  # 天合光能
            "300253.SZ": 0.10,  # 卫宁健康
        },
        # 指增策略配置
        "mars_v8_300_指增": {
            "600519.SH": 0.30,  # 贵州茅台
            "000858.SZ": 0.25,  # 五粮液
            "600036.SH": 0.20,  # 招商银行
            "000001.SZ": 0.15,  # 平安银行
            "600276.SH": 0.10,  # 恒瑞医药
        },
        "rossa_v5_300_指增": {
            "600519.SH": 0.28,  # 贵州茅台
            "000858.SZ": 0.22,  # 五粮液
            "600036.SH": 0.20,  # 招商银行
            "600276.SH": 0.15,  # 恒瑞医药
            "000001.SZ": 0.15,  # 平安银行
        },
    }


def simulate_advanced_fund_operations():
    """模拟高级基金运作过程"""

    print("🚀 创建高级策略树（只有根节点和叶子节点有账户）")
    print("=" * 80)

    fund = create_advanced_strategy_tree()
    strategy_allocations = get_strategy_allocations()

    print("初始账户状态:")
    fund.print_account_details()

    print("\n" + "=" * 80)
    print("📈 第一步：申购操作 - 5000万")
    print("=" * 80)

    subscription_amount = 50000000
    print(f"客户申购: {subscription_amount:,.2f} 元")
    fund.process_subscription(subscription_amount)

    print("\n申购后账户状态:")
    fund.print_account_details()

    print("\n" + "=" * 80)
    print("🏗️ 第二步：建仓操作")
    print("=" * 80)

    print("开始为各策略建仓...")
    fund.build_positions_from_pending(strategy_allocations)

    print("\n建仓后账户状态:")
    fund.print_account_details()

    print("\n" + "=" * 80)
    print("🔥 第2.5步：期货初始建仓")
    print("=" * 80)

    print("根据敞口要求进行期货初始建仓...")
    fund.rebalance_futures_positions()

    print("\n期货建仓后账户状态:")
    fund.print_account_details()

    print("\n期货持仓详情:")
    fund.print_futures_details()

    print("\n" + "=" * 80)
    print("🔄 第三步：高级交易系统调仓")
    print("=" * 80)

    # 模拟市场信号变化后的高级调仓
    print("模拟市场变化，策略信号调整...")

    # 市场信号：减持贵州茅台，增持科技股
    market_signals = {
        "mars_v8_300": {
            "000001.SZ": 0.05,  # 平安银行 +5%
            "000002.SZ": -0.02,  # 万科A -2%
            "000858.SZ": -0.03,  # 五粮液 -3%
            "600519.SH": -0.05,  # 贵州茅台 -5%
            "600036.SH": 0.05,  # 招商银行 +5%
        },
        "titan_v2_500": {
            "002415.SZ": -0.05,  # 海康威视 -5%
            "002594.SZ": 0.05,  # 比亚迪 +5%
            "300059.SZ": 0.03,  # 东方财富 +3%
            "300750.SZ": 0.05,  # 宁德时代 +5%
            "002230.SZ": 0.00,  # 科大讯飞 保持
        },
        "rossa_v5_300": {
            "600519.SH": -0.03,  # 贵州茅台 -3%
            "000858.SZ": -0.02,  # 五粮液 -2%
            "600036.SH": 0.02,  # 招商银行 +2%
            "600276.SH": 0.03,  # 恒瑞医药 +3%
        },
    }

    from src.entity.strategy import TradingSystem

    # 创建交易系统（80%成交率，0.1%滑点）
    trading_system = TradingSystem(execution_rate=0.8, slippage_rate=0.001)

    fund.advanced_rebalance(market_signals, trading_system)

    print("\n高级调仓后账户状态:")
    fund.print_account_details()

    print("\n" + "=" * 80)
    print("🔥 第3.5步：期货调仓（响应股票仓位变化）")
    print("=" * 80)

    print("股票仓位变化后，调整期货对冲...")
    fund.rebalance_futures_positions()

    print("\n期货调仓后持仓详情:")
    fund.print_futures_details()

    print("\n" + "=" * 80)
    print("💰 第四步：新申购 + 全面建仓")
    print("=" * 80)

    # 新申购2000万
    new_subscription = 20000000
    print(f"新申购: {new_subscription:,.2f} 元")
    fund.process_subscription(new_subscription)

    # 为新申购资金建仓
    print("\n为新申购资金建仓:")
    fund.build_positions_from_pending(strategy_allocations)

    print("\n新申购建仓后账户状态:")
    fund.print_account_details()

    print("\n" + "=" * 80)
    print("🔥 第4.5步：期货调仓（响应新申购资金）")
    print("=" * 80)

    print("新申购资金建仓后，调整期货对冲...")
    fund.rebalance_futures_positions()

    print("\n最终期货持仓详情:")
    fund.print_futures_details()

    print("\n" + "=" * 80)
    print("💸 第五步：赎回模拟")
    print("=" * 80)

    # 模拟客户赎回1500万
    redemption_amount = 15000000
    print(f"模拟客户赎回 {redemption_amount:,.2f} 元")
    fund.process_redemption(redemption_amount)

    print("\n赎回后账户状态:")
    fund.print_account_details()

    print("\n" + "=" * 80)
    print("📊 最终统计分析")
    print("=" * 80)

    # 获取根节点和叶子节点摘要
    root_summary = fund.get_account_summary()

    def collect_leaf_summaries(strategy: StrategyTree, summaries: list | None = None):
        if summaries is None:
            summaries = []

        if not strategy.children:  # 叶子节点
            summary = strategy.get_account_summary()
            summaries.append(summary)
        else:
            for child in strategy.children:
                collect_leaf_summaries(child, summaries)

        return summaries

    leaf_summaries = collect_leaf_summaries(fund)

    print(f"📈 基金总资产（根节点统计）: {root_summary['total_value']:,.2f} 元")
    print(f"📊 申购总额: {subscription_amount + new_subscription:,.2f} 元")
    print(f"📉 赎回总额: {redemption_amount:,.2f} 元")
    print(f"📊 净申购金额: {subscription_amount + new_subscription - redemption_amount:,.2f} 元")
    print(
        f"✅ 资产匹配检查: {'正确' if abs(root_summary['total_value'] - (subscription_amount + new_subscription - redemption_amount)) < 1000 else '异常'}"
    )

    print(f"\n📋 叶子节点明细（共{len(leaf_summaries)}个策略）:")
    leaf_total = 0
    for summary in leaf_summaries:
        if summary["total_value"] > 0:  # 只显示有资产的
            print(
                f"  {summary['name']:25} | 资产: {summary['total_value']:>12,.2f} 元 | 持仓: {summary['stock_positions']}只"
            )
            leaf_total += summary["total_value"]

    print(f"\n💎 叶子节点资产合计: {leaf_total:,.2f} 元")
    print(
        f"🔍 根节点vs叶子节点: {'一致' if abs(root_summary['total_value'] - leaf_total) < 1000 else '不一致'}"
    )

    # 按策略类型分类统计
    print("\n📈 按策略类型统计:")
    strategy_types = {}
    for summary in leaf_summaries:
        if summary["total_value"] > 0:
            strategy_type = (
                summary["name"].split("_")[0] if "_" in summary["name"] else summary["name"][:10]
            )
            strategy_types[strategy_type] = (
                strategy_types.get(strategy_type, 0) + summary["total_value"]
            )

    for strategy_type, total_value in sorted(
        strategy_types.items(), key=lambda x: x[1], reverse=True
    ):
        percentage = (total_value / root_summary["total_value"]) * 100
        print(f"  {strategy_type:15} | {total_value:>12,.2f} 元 ({percentage:5.1f}%)")

    # 交易系统统计
    print(f"\n🔧 交易系统统计:")
    print(f"  系统成交率: 80%")
    print(f"  滑点设置: 0.1%")
    print(f"  内部自成交: 支持")
    print(f"  未成交处理: 按权重分配")


def test_weight_validation():
    """测试权重验证"""
    print("\n" + "=" * 80)
    print("🔍 权重验证测试")
    print("=" * 80)

    fund = create_advanced_strategy_tree()

    try:
        fund.validate_weights()
        print("✅ 权重验证通过")
    except ValueError as e:
        print(f"❌ 权重验证失败: {e}")


if __name__ == "__main__":
    print("🎯 高级策略树模拟系统")
    print("=" * 80)

    # 运行模拟
    simulate_advanced_fund_operations()

    # 验证权重
    test_weight_validation()

    print("\n✨ 高级模拟完成！")
