from typing import Dict, List, Optional

import matplotlib.pyplot as plt  # type: ignore
import networkx as nx  # type: ignore

# 添加 Plotly 导入和 treemap 函数
import plotly.graph_objects as go  # type: ignore
from graphviz import Digraph  # type: ignore
from networkx.drawing.nx_agraph import graphviz_layout  # type: ignore

from src.entity.strategy import StrategyTree, VirtualAccount  # Import VirtualAccount for type hint


def build_main_label(node: StrategyTree) -> str:
    """构建主节点标签（record 格式）。"""
    # 更新为更明确的纵向排列：使用嵌套 record 强调垂直
    return (
        "{Main Node | {"
        + f"Name: {node.name} | Fund ID: {node.fund_id} | Weight: {node.weight:.2f}"
        + "}}"
    )


def build_account_label(va: VirtualAccount) -> str | None:
    """构建 account 小 UI 标签（record 格式），如果为空返回 None。"""
    if not va or (not va.cash_info and not va.stock_long_info and not va.futures_short_info):
        return None  # 早返回：无数据不创建

    lines = []
    if va.cash_info:
        lines.append(f"Cash: {va.cash_info.get('amount', 0):.2f}")
    lines.append(f"Stock Long: {len(va.stock_long_info) if va.stock_long_info else 0} items")
    lines.append(
        f"Futures Short: {len(va.futures_short_info) if va.futures_short_info else 0} items"
    )
    lines.append(f"Pending: {va.pending_purchase_amount:.2f}")

    # 更新为更明确的纵向排列：使用嵌套 record 强调垂直
    return "{Account | {" + "|".join(lines) + "}}"


def generate_tree_dot(
    node: StrategyTree,
    graph: Digraph | None = None,
    parent_id: str | None = None,
    show_account_ui: bool = True,
    account_style: dict = {
        "shape": "Mrecord",
        "fillcolor": "lightcyan",
        "fontsize": "10",
    },  # 默认颜色 lightcyan
) -> Digraph:
    """递归生成 Graphviz DOT 图，支持 account 小 UI，并区分形态。

    Args:
        node: StrategyTree 节点
        graph: Graphviz 图对象 (首次调用时为 None)
        parent_id: 父节点 ID (用于连接)
        show_account_ui: 是否显示 account 小 UI
        account_style: 账户节点样式字典（可自定义形状、颜色等）

    Returns:
        生成的 Graphviz 图对象
    """
    if not isinstance(node, StrategyTree):
        raise ValueError("无效节点类型，必须为 StrategyTree")

    if graph is None:
        graph = Digraph(comment="Strategy Tree", format="png")
        graph.attr(rankdir="TB")  # 改回垂直布局以保持树状层次
        # 主节点全局样式：矩形表格，浅蓝
        graph.attr(
            "node",
            shape="record",
            style="filled",
            fillcolor="lightblue",
            fontname="Arial",
            fontsize="12",
        )
        graph.attr("edge", arrowhead="normal", color="gray")

    # 创建主节点（矩形表格，浅蓝）
    node_id = f"{node.name}_{node.fund_id}"
    graph.node(node_id, label=build_main_label(node))

    if parent_id:
        graph.edge(parent_id, node_id)  # 主树边：实线箭头

    # 创建 account 小 UI（圆角矩形表格，自定义颜色，作为附属）
    if show_account_ui:
        account_label = build_account_label(node.virtual_account)
        if account_label:
            with graph.subgraph(name=f"cluster_{node_id}") as c:
                c.attr(rank="same")  # 强制主节点和 account 节点横向并排
                c.attr(style="dashed", color="lightgray", label="")  # 虚线框分组
                account_id = f"account_{node_id}"
                # 应用自定义样式：区分形态
                c.node(
                    account_id,
                    label=account_label,
                    style="filled",
                    **account_style,  # e.g., shape="Mrecord", fillcolor="lightcyan"
                )
                c.edge(
                    node_id, account_id, style="dashed", arrowhead="none", label="account"
                )  # 附属边：虚线无箭头

    # 递归子节点，保持主树结构
    for child in node.children:
        generate_tree_dot(child, graph, node_id, show_account_ui, account_style)

    return graph


def visualize_strategy_tree_graphviz(
    tree: StrategyTree,
    output_file: str = "docs/strategy_tree.png",
    show_account_ui: bool = True,
    account_style: dict = {
        "shape": "Mrecord",
        "fillcolor": "lightcyan",
        "fontsize": "10",
    },  # 默认颜色 lightcyan
) -> str:
    """使用 Graphviz 可视化 StrategyTree 并保存为图像，返回文件路径。"""
    dot = generate_tree_dot(tree, show_account_ui=show_account_ui, account_style=account_style)
    dot.render(output_file, view=True, cleanup=True)
    return output_file


# 更新 flatten_tree_for_treemap 函数
def flatten_tree_for_treemap(
    node: StrategyTree,
    parent_id: str = "",
    ids: list[str] | None = None,
    labels: list[str] | None = None,
    parents: list[str] | None = None,
    values: list[float] | None = None,
    hovertexts: list[str] | None = None,
) -> dict[str, list]:
    """递归扁平化 StrategyTree 为 treemap 数据。"""
    if ids is None:
        ids = []
    if labels is None:
        labels = []
    if parents is None:
        parents = []
    if values is None:
        values = []
    if hovertexts is None:
        hovertexts = []

    node_id = f"{node.name}_{node.fund_id}"
    label = f"{node.name} (ID: {node.fund_id})"
    value = max(node.weight, 0.01)  # 确保正值以渲染可见矩形
    hovertext = f"Weight: {node.weight:.2f}<br>Account: Cash {node.virtual_account.cash_info.get('amount', 0) if node.virtual_account.cash_info else 'N/A'}<br>Stock Long: {len(node.virtual_account.stock_long_info) if node.virtual_account.stock_long_info else 0} items"

    ids.append(node_id)
    labels.append(label)
    parents.append(parent_id)
    values.append(value)
    hovertexts.append(hovertext)

    for child in node.children:
        flatten_tree_for_treemap(child, node_id, ids, labels, parents, values, hovertexts)

    return {
        "ids": ids,
        "labels": labels,
        "parents": parents,
        "values": values,
        "hovertexts": hovertexts,
    }


def visualize_strategy_tree_treemap(
    tree: StrategyTree, output_file: str = "docs/strategy_treemap.html"
) -> str:
    """使用 Plotly 生成交互式 treemap 可视化，并保存为 HTML 文件。"""
    data = flatten_tree_for_treemap(tree)
    print("Treemap Data:", data)  # Debug: 打印数据以检查是否为空
    fig = go.Figure(
        go.Treemap(
            ids=data["ids"],
            labels=data["labels"],
            parents=data["parents"],
            values=data["values"],
            text=data["hovertexts"],  # 设置 text 为 hovertexts 以显示悬停信息
            hoverinfo="text",
            textinfo="label+value",
            textfont_size=12,
            marker_colorscale="Blues",  # 柔和颜色方案
            branchvalues="total",
            tiling={"packing": "squarify"},  # 矩形树图布局
        )
    )
    fig.update_layout(title="Strategy Tree Treemap", margin=dict(t=50, l=25, r=25, b=25))
    fig.write_html(output_file)
    fig.show()  # Debug: 在浏览器中打开以检查渲染
    return output_file
