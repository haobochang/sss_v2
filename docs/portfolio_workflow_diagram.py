#!/usr/bin/env python3
"""
投资组合节点树运作流程图生成器
使用matplotlib绘制详细的时序图和状态转换图
"""

from datetime import datetime, timedelta

import matplotlib.dates as mdates
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import ConnectionPatch, FancyBboxPatch

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["SimHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def create_portfolio_tree_diagram():
    """创建投资组合树状结构图"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # 定义节点位置和样式
    nodes = {
        "product": {
            "pos": (5, 9),
            "size": (3, 0.8),
            "color": "#FF6B6B",
            "text": "量化产品A\n总资金: 1000万",
        },
        "neutral": {
            "pos": (2, 7),
            "size": (2.5, 0.6),
            "color": "#4ECDC4",
            "text": "中性策略组\n权重: 50%\n资金: 500万",
        },
        "timing": {
            "pos": (8, 7),
            "size": (2.5, 0.6),
            "color": "#45B7D1",
            "text": "择时策略组\n权重: 50%\n资金: 500万",
        },
        "base1": {
            "pos": (1, 5),
            "size": (2, 0.5),
            "color": "#96CEB4",
            "text": "多因子策略\n权重: 33.3%\n资金: 167万",
        },
        "base2": {
            "pos": (3, 5),
            "size": (2, 0.5),
            "color": "#96CEB4",
            "text": "统计套利\n权重: 33.3%\n资金: 167万",
        },
        "base3": {
            "pos": (7, 5),
            "size": (2, 0.5),
            "color": "#FFEAA7",
            "text": "趋势跟踪\n权重: 50%\n资金: 250万",
        },
        "base4": {
            "pos": (9, 5),
            "size": (2, 0.5),
            "color": "#FFEAA7",
            "text": "反转策略\n权重: 50%\n资金: 250万",
        },
    }

    # 绘制节点
    for node_id, node_info in nodes.items():
        x, y = node_info["pos"]
        w, h = node_info["size"]
        color = node_info["color"]
        text = node_info["text"]

        # 绘制节点框
        box = FancyBboxPatch(
            (x - w / 2, y - h / 2),
            w,
            h,
            boxstyle="round,pad=0.1",
            facecolor=color,
            edgecolor="black",
            linewidth=2,
            alpha=0.8,
        )
        ax.add_patch(box)

        # 添加文本
        ax.text(x, y, text, ha="center", va="center", fontsize=10, fontweight="bold")

    # 绘制连接线
    connections = [
        ("product", "neutral"),
        ("product", "timing"),
        ("neutral", "base1"),
        ("neutral", "base2"),
        ("timing", "base3"),
        ("timing", "base4"),
    ]

    for parent, child in connections:
        parent_pos = nodes[parent]["pos"]
        child_pos = nodes[child]["pos"]

        # 绘制箭头
        arrow = ConnectionPatch(
            parent_pos,
            child_pos,
            "data",
            "data",
            arrowstyle="->",
            shrinkA=5,
            shrinkB=5,
            mutation_scale=20,
            fc="black",
            linewidth=2,
        )
        ax.add_patch(arrow)

    # 添加标题
    ax.text(5, 9.8, "投资组合节点树结构", ha="center", va="center", fontsize=16, fontweight="bold")

    plt.tight_layout()
    plt.savefig("docs/portfolio_tree_structure.png", dpi=300, bbox_inches="tight")
    plt.show()


def create_workflow_timeline():
    """创建工作流程时序图"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 8))

    # 定义时间轴
    start_time = datetime(2024, 1, 1, 8, 0)
    end_time = datetime(2024, 1, 1, 16, 0)

    # 定义流程阶段
    stages = [
        {"name": "盘前计算\n(Bottom-up)", "start": "08:30", "end": "09:00", "color": "#FF6B6B"},
        {
            "name": "生成交易指令\n(Aggregation)",
            "start": "09:00",
            "end": "09:30",
            "color": "#4ECDC4",
        },
        {"name": "交易执行\n(Execution)", "start": "09:30", "end": "15:00", "color": "#45B7D1"},
        {"name": "结果分发\n(Top-down)", "start": "15:30", "end": "16:00", "color": "#96CEB4"},
    ]

    # 绘制时间轴
    ax.set_xlim(mdates.date2num(start_time), mdates.date2num(end_time))
    ax.set_ylim(0, 5)

    # 格式化时间轴
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

    # 绘制阶段块
    y_positions = [4, 3, 2, 1]
    for i, (stage, y_pos) in enumerate(zip(stages, y_positions)):
        start_str = stage["start"]
        end_str = stage["end"]

        start_dt = datetime.strptime(f"2024-01-01 {start_str}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"2024-01-01 {end_str}", "%Y-%m-%d %H:%M")

        # 绘制阶段块
        rect = patches.Rectangle(
            (mdates.date2num(start_dt), y_pos - 0.3),
            mdates.date2num(end_dt) - mdates.date2num(start_dt),
            0.6,
            facecolor=stage["color"],
            edgecolor="black",
            linewidth=2,
            alpha=0.8,
        )
        ax.add_patch(rect)

        # 添加阶段名称
        center_time = start_dt + (end_dt - start_dt) / 2
        ax.text(
            mdates.date2num(center_time),
            y_pos,
            stage["name"],
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
        )

    # 添加数据流转箭头
    data_flows = [
        {"from": "08:30", "to": "09:00", "text": "Alpha模型\n生成目标持仓", "y": 4.5},
        {"from": "09:00", "to": "09:30", "text": "权重聚合\n计算调仓需求", "y": 3.5},
        {"from": "09:30", "to": "15:00", "text": "执行交易\n更新订单状态", "y": 2.5},
        {"from": "15:30", "to": "16:00", "text": "分发结果\n更新实际持仓", "y": 1.5},
    ]

    for flow in data_flows:
        start_dt = datetime.strptime(f"2024-01-01 {flow['from']}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"2024-01-01 {flow['to']}", "%Y-%m-%d %H:%M")

        # 绘制箭头
        ax.annotate(
            "",
            xy=(end_dt, flow["y"]),
            xytext=(start_dt, flow["y"]),
            arrowprops=dict(arrowstyle="->", lw=2, color="red"),
        )

        # 添加说明文字
        center_time = start_dt + (end_dt - start_dt) / 2
        ax.text(
            center_time,
            flow["y"] + 0.1,
            flow["text"],
            ha="center",
            va="bottom",
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
        )

    # 设置标题和标签
    ax.set_title("量化系统日度工作流程时序图", fontsize=16, fontweight="bold", pad=20)
    ax.set_ylabel("流程阶段", fontsize=12)
    ax.set_xlabel("时间", fontsize=12)

    # 隐藏y轴刻度
    ax.set_yticks([])

    plt.tight_layout()
    plt.savefig("docs/workflow_timeline.png", dpi=300, bbox_inches="tight")
    plt.show()


def create_data_flow_diagram():
    """创建数据流转图"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # 定义组件位置
    components = {
        "alpha_model": {
            "pos": (2, 8),
            "size": (2, 1),
            "color": "#FF6B6B",
            "text": "Alpha模型\n生成因子",
        },
        "base_strategy": {
            "pos": (2, 6),
            "size": (2, 1),
            "color": "#4ECDC4",
            "text": "基准策略层\n目标持仓",
        },
        "strategy_pool": {
            "pos": (6, 6),
            "size": (2, 1),
            "color": "#45B7D1",
            "text": "策略组合层\n权重聚合",
        },
        "product": {"pos": (6, 8), "size": (2, 1), "color": "#96CEB4", "text": "产品层\n调仓指令"},
        "trade_system": {
            "pos": (6, 4),
            "size": (2, 1),
            "color": "#FFEAA7",
            "text": "交易系统\n执行交易",
        },
        "actual_pos": {"pos": (2, 4), "size": (2, 1), "color": "#DDA0DD", "text": "实际持仓\n更新"},
    }

    # 绘制组件
    for comp_id, comp_info in components.items():
        x, y = comp_info["pos"]
        w, h = comp_info["size"]
        color = comp_info["color"]
        text = comp_info["text"]

        # 绘制组件框
        box = FancyBboxPatch(
            (x - w / 2, y - h / 2),
            w,
            h,
            boxstyle="round,pad=0.1",
            facecolor=color,
            edgecolor="black",
            linewidth=2,
            alpha=0.8,
        )
        ax.add_patch(box)

        # 添加文本
        ax.text(x, y, text, ha="center", va="center", fontsize=10, fontweight="bold")

    # 定义数据流
    flows = [
        # 向上聚合流
        {"from": "alpha_model", "to": "base_strategy", "label": "Alpha因子", "color": "blue"},
        {"from": "base_strategy", "to": "strategy_pool", "label": "目标持仓", "color": "green"},
        {"from": "strategy_pool", "to": "product", "label": "聚合持仓", "color": "green"},
        {"from": "product", "to": "trade_system", "label": "调仓指令", "color": "red"},
        # 向下分发流
        {"from": "trade_system", "to": "actual_pos", "label": "执行结果", "color": "orange"},
        {"from": "actual_pos", "to": "base_strategy", "label": "实际持仓", "color": "purple"},
    ]

    # 绘制数据流箭头
    for flow in flows:
        from_pos = components[flow["from"]]["pos"]
        to_pos = components[flow["to"]]["pos"]

        # 绘制箭头
        arrow = ConnectionPatch(
            from_pos,
            to_pos,
            "data",
            "data",
            arrowstyle="->",
            shrinkA=5,
            shrinkB=5,
            mutation_scale=20,
            fc=flow["color"],
            linewidth=2,
            color=flow["color"],
        )
        ax.add_patch(arrow)

        # 添加标签
        mid_x = (from_pos[0] + to_pos[0]) / 2
        mid_y = (from_pos[1] + to_pos[1]) / 2
        ax.text(
            mid_x,
            mid_y + 0.2,
            flow["label"],
            ha="center",
            va="center",
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
        )

    # 添加标题
    ax.text(6, 9.5, "数据流转示意图", ha="center", va="center", fontsize=16, fontweight="bold")

    # 添加说明
    ax.text(
        1,
        1,
        "蓝色: Alpha因子流\n绿色: 目标持仓聚合流\n红色: 交易指令流\n橙色: 执行结果流\n紫色: 实际持仓更新流",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8),
    )

    plt.tight_layout()
    plt.savefig("docs/data_flow_diagram.png", dpi=300, bbox_inches="tight")
    plt.show()


def create_position_tracking_diagram():
    """创建持仓跟踪示意图"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # 左图：持仓类型对比
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis("off")

    # 绘制TARGET持仓
    target_box = FancyBboxPatch(
        (1, 6), 3, 2, boxstyle="round,pad=0.1", facecolor="#FF6B6B", edgecolor="black", linewidth=2
    )
    ax1.add_patch(target_box)
    ax1.text(
        2.5, 7, "TARGET持仓\n(目标持仓)", ha="center", va="center", fontsize=12, fontweight="bold"
    )

    # 绘制ACTUAL持仓
    actual_box = FancyBboxPatch(
        (6, 6), 3, 2, boxstyle="round,pad=0.1", facecolor="#4ECDC4", edgecolor="black", linewidth=2
    )
    ax1.add_patch(actual_box)
    ax1.text(
        7.5, 7, "ACTUAL持仓\n(实际持仓)", ha="center", va="center", fontsize=12, fontweight="bold"
    )

    # 添加对比说明
    ax1.text(5, 4, "持仓类型对比", ha="center", va="center", fontsize=14, fontweight="bold")
    ax1.text(
        2.5, 3, "• 模型计算得出\n• 优化器生成\n• 理想状态", ha="center", va="center", fontsize=10
    )
    ax1.text(7.5, 3, "• 交易执行后\n• 市场实际\n• 真实状态", ha="center", va="center", fontsize=10)

    # 右图：层级持仓示例
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis("off")

    # 绘制层级结构
    levels = [
        {"y": 8, "text": "产品层: 000001(1000股)", "color": "#FF6B6B"},
        {"y": 6, "text": "中性策略: 000001(500股)", "color": "#4ECDC4"},
        {"y": 4, "text": "多因子策略: 000001(300股)", "color": "#45B7D1"},
        {"y": 2, "text": "统计套利: 000001(200股)", "color": "#96CEB4"},
    ]

    for i, level in enumerate(levels):
        box = FancyBboxPatch(
            (1, level["y"] - 0.5),
            8,
            1,
            boxstyle="round,pad=0.1",
            facecolor=level["color"],
            edgecolor="black",
            linewidth=2,
            alpha=0.8,
        )
        ax2.add_patch(box)
        ax2.text(
            5, level["y"], level["text"], ha="center", va="center", fontsize=11, fontweight="bold"
        )

        # 添加权重说明
        if i < len(levels) - 1:
            ax2.text(
                9.5, level["y"], f"权重\n{100 / (i + 1):.0f}%", ha="center", va="center", fontsize=9
            )

    ax2.text(
        5,
        9.5,
        "层级持仓示例 (000001股票)",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
    )

    plt.tight_layout()
    plt.savefig("docs/position_tracking_diagram.png", dpi=300, bbox_inches="tight")
    plt.show()


def main():
    """生成所有图表"""
    print("正在生成投资组合节点树方案分析图表...")

    # 创建docs目录
    import os

    os.makedirs("docs", exist_ok=True)

    # 生成各种图表
    create_portfolio_tree_diagram()
    create_workflow_timeline()
    create_data_flow_diagram()
    create_position_tracking_diagram()

    print("图表生成完成！")
    print("生成的文件：")
    print("- docs/portfolio_tree_structure.png")
    print("- docs/workflow_timeline.png")
    print("- docs/data_flow_diagram.png")
    print("- docs/position_tracking_diagram.png")


if __name__ == "__main__":
    main()
