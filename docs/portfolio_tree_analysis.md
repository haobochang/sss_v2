# 统一投资组合节点树方案分析

## 方案概述

这个方案通过抽象化和统一化，将传统的分散式策略配置重构为一个统一的树状结构，实现了：

1. **统一的层级结构**：产品 → 投资策略 → 策略组合 → 基准策略
2. **统一的持仓跟踪**：一张表记录所有层级的真实/虚拟持仓
3. **清晰的聚合与分发路径**：交易指令从下往上聚合，回执从上往下分发

## 核心数据模型

### 1. PortfolioNode（投资组合节点）
```python
class PortfolioNode(BaseMongoModel):
    name: str                    # 节点名称
    node_type: str              # 节点类型：PRODUCT, INVESTMENT_STRATEGY, STRATEGY_POOL, BASE_STRATEGY
    config_details: dict        # 配置详情（JSON格式）
    source_id: int              # 关联源ID
    status: int                 # 状态：1启用，0禁用
```

### 2. PortfolioHierarchy（层级关系）
```python
class PortfolioHierarchy(BaseMongoModel):
    parent_node_id: ObjectId    # 父节点ID
    child_node_id: ObjectId     # 子节点ID
    weight: Decimal             # 权重
    start_date: datetime        # 生效日期
    end_date: datetime          # 失效日期
```

### 3. NodePosition（统一持仓）
```python
class NodePosition(BaseMongoModel):
    node_id: ObjectId           # 节点ID
    trading_day: datetime       # 交易日
    symbol: str                 # 证券代码
    position_type: str          # 持仓类型：TARGET（目标）, ACTUAL（实际）
    quantity: Decimal           # 持仓数量
    cost_price: Decimal         # 成本价
    market_value: Decimal       # 市值
    weight_in_node: Decimal     # 在节点内权重
```

### 4. TradeOrder & TradeAllocation（交易与分配）
```python
class TradeOrder(BaseMongoModel):
    product_node_id: ObjectId   # 产品节点ID
    trading_day: datetime       # 交易日
    basket_id: str              # 篮子ID
    symbol: str                 # 证券代码
    target_quantity: Decimal    # 目标数量
    filled_quantity: Decimal    # 成交数量
    status: str                 # 状态

class TradeAllocation(BaseMongoModel):
    order_id: ObjectId          # 订单ID
    leaf_node_id: ObjectId      # 叶子节点ID
    allocated_quantity: Decimal # 分配数量
```

## 架构示意图

```
┌─────────────────────────────────────────────────────────────────┐
│                        量化产品A (PRODUCT)                        │
│                        总资金: 1000万                            │
└─────────────────────┬───────────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
┌───────▼────────┐        ┌────────▼────────┐
│   中性策略组     │        │   择时策略组     │
│   权重: 50%     │        │   权重: 50%     │
│   资金: 500万   │        │   资金: 500万   │
└───────┬────────┘        └────────┬────────┘
        │                          │
    ┌───┴───┐                  ┌───┴───┐
    │       │                  │       │
┌───▼───┐ ┌─▼───┐          ┌───▼───┐ ┌─▼───┐
│基准1  │ │基准2 │          │基准1  │ │基准2 │
│33.3%  │ │33.3%│          │50%    │ │50%   │
│167万  │ │167万│          │250万  │ │250万 │
└───────┘ └─────┘          └───────┘ └─────┘
```

## 真实场景运作流程

### 场景：某量化基金产品A的日度调仓

#### 1. 盘前计算阶段（Bottom-up）

```
时间：T日 08:30
目标：计算各层级的目标持仓
```

**步骤1：基准策略层计算**
```python
# 每个基准策略运行模型，生成Alpha
for base_strategy in base_strategies:
    alpha_dict = alpha_model.generate_alpha(date, universe)
    
    # 根据Alpha计算目标持仓
    for symbol, alpha in alpha_dict.items():
        target_weight = alpha * leverage
        target_quantity = allocated_capital * target_weight / price
        
        # 写入目标持仓
        NodePosition(
            node_id=base_strategy.id,
            trading_day=date,
            symbol=symbol,
            position_type="TARGET",
            quantity=target_quantity
        ).insert()
```

**步骤2：向上聚合计算**
```python
# 从叶子节点向上聚合，计算上层节点的目标持仓
def aggregate_positions(node_id: ObjectId, date: datetime):
    children = get_children(node_id)
    aggregated_positions = {}
    
    for child in children:
        child_positions = get_node_positions(child.id, date, "TARGET")
        weight = get_hierarchy_weight(node_id, child.id)
        
        for pos in child_positions:
            if pos.symbol not in aggregated_positions:
                aggregated_positions[pos.symbol] = 0
            aggregated_positions[pos.symbol] += pos.quantity * weight
    
    # 写入聚合后的目标持仓
    for symbol, quantity in aggregated_positions.items():
        NodePosition(
            node_id=node_id,
            trading_day=date,
            symbol=symbol,
            position_type="TARGET",
            quantity=quantity
        ).insert()
```

#### 2. 生成交易指令阶段（Aggregation）

```
时间：T日 09:00
目标：在产品层生成调仓指令
```

**步骤1：计算产品层调仓需求**
```python
# 比较产品层的目标持仓和实际持仓
product_target = get_node_positions(product_id, date, "TARGET")
product_actual = get_node_positions(product_id, date, "ACTUAL")

for symbol in set(product_target.keys()) | set(product_actual.keys()):
    target_qty = product_target.get(symbol, 0)
    actual_qty = product_actual.get(symbol, 0)
    trade_qty = target_qty - actual_qty
    
    if abs(trade_qty) > min_trade_threshold:
        # 创建产品层交易指令
        order = TradeOrder(
            product_node_id=product_id,
            trading_day=date,
            basket_id=f"basket_{date.strftime('%Y%m%d')}",
            symbol=symbol,
            target_quantity=trade_qty,
            status="PENDING"
        ).insert()
```

**步骤2：计算底层贡献**
```python
# 计算每个叶子节点对产品层交易的贡献
def calculate_leaf_contributions(order_id: ObjectId):
    order = TradeOrder.find_by_id(order_id)
    leaf_nodes = get_leaf_nodes(product_id)
    
    for leaf in leaf_nodes:
        # 计算该叶子节点对产品层持仓的贡献权重
        contribution_weight = calculate_contribution_weight(leaf.id, product_id)
        
        # 分配交易数量
        allocated_qty = order.target_quantity * contribution_weight
        
        TradeAllocation(
            order_id=order_id,
            leaf_node_id=leaf.id,
            allocated_quantity=allocated_qty
        ).insert()
```

#### 3. 交易执行阶段

```
时间：T日 09:30-15:00
目标：执行产品层交易指令
```

```python
# 交易执行（实际由交易系统处理）
for order in pending_orders:
    # 执行交易
    execution_result = execute_trade(order)
    
    # 更新订单状态
    order.filled_quantity = execution_result.filled_qty
    order.status = "FILLED"
    order.update()
```

#### 4. 结果分发阶段（Top-down）

```
时间：T日 15:30
目标：将执行结果分发到各层级虚拟账户
```

**步骤1：更新叶子节点实际持仓**
```python
# 根据TradeAllocation更新叶子节点的实际持仓
for allocation in TradeAllocation.find_by_order_id(order_id):
    leaf_node = PortfolioNode.find_by_id(allocation.leaf_node_id)
    
    # 更新叶子节点的实际持仓
    current_pos = get_node_position(leaf_node.id, symbol, "ACTUAL")
    new_quantity = current_pos.quantity + allocation.allocated_quantity
    
    NodePosition(
        node_id=leaf_node.id,
        trading_day=date,
        symbol=symbol,
        position_type="ACTUAL",
        quantity=new_quantity
    ).insert()
```

**步骤2：向上聚合更新**
```python
# 从叶子节点向上聚合，更新所有上层节点的实际持仓
def update_actual_positions(date: datetime):
    # 按层级顺序更新（从底层到顶层）
    levels = get_node_levels()
    
    for level in sorted(levels):
        nodes = get_nodes_by_level(level)
        for node in nodes:
            aggregate_actual_positions(node.id, date)
```

## 数据流转示意图

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   基准策略层     │    │   策略组合层     │    │     产品层      │
│                 │    │                 │    │                 │
│ Alpha模型       │───▶│   权重聚合       │───▶│   目标持仓      │
│ 生成目标持仓     │    │   计算目标持仓   │    │   计算调仓需求   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   实际持仓       │    │   实际持仓       │    │   实际持仓       │
│                 │    │                 │    │                 │
│ 更新实际持仓     │◀───│   权重聚合       │◀───│   交易执行      │
│ 记录盈亏         │    │   更新实际持仓   │    │   分发结果      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 优势分析

### 1. 结构清晰
- **统一模型**：所有层级使用相同的节点模型
- **关系明确**：通过PortfolioHierarchy明确定义父子关系和权重
- **版本管理**：支持配置的时效性管理

### 2. 跟踪灵活
- **一张表搞定**：NodePosition记录所有层级的持仓
- **类型区分**：TARGET和ACTUAL区分目标持仓和实际持仓
- **历史回溯**：支持任意日期的持仓查询

### 3. 路径明确
- **聚合路径**：TradeAllocation记录交易的来源
- **分发路径**：执行结果按权重分发到各层级
- **审计完整**：完整的交易链路追踪

### 4. 易于扩展
- **新增层级**：只需在PortfolioNode中增加node_type
- **新增策略**：通过配置节点快速添加
- **参数调整**：通过config_details灵活配置

## 实际应用场景

### 场景1：多策略产品管理
```
产品A（1000万）
├── 中性策略（500万）
│   ├── 多因子策略（250万）
│   └── 统计套利（250万）
└── 择时策略（500万）
    ├── 趋势跟踪（300万）
    └── 反转策略（200万）
```

### 场景2：策略权重调整
```python
# 调整中性策略权重从50%到60%
new_hierarchy = PortfolioHierarchy(
    parent_node_id=product_id,
    child_node_id=neutral_strategy_id,
    weight=Decimal("0.6"),
    start_date=adjustment_date
)
```

### 场景3：回测分析
```python
# 查询任意日期的策略表现
def analyze_strategy_performance(strategy_id: ObjectId, start_date: datetime, end_date: datetime):
    positions = NodePosition.find_by_node_and_date_range(
        strategy_id, start_date, end_date, "ACTUAL"
    )
    return calculate_performance_metrics(positions)
```

## 总结

这个统一投资组合节点树方案通过抽象化和标准化，完美解决了量化系统中的层级管理、持仓跟踪和交易分配问题。它不仅简化了数据结构，还提供了清晰的业务逻辑路径，是一个高度可扩展和可维护的解决方案。 