from __future__ import annotations

from datetime import date, datetime
from enum import Enum

from sqlalchemy import (
    DATETIME,
    DECIMAL,
    Double,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


class AssetType(str, Enum):
    """资产类型枚举"""

    STOCK = "stock"  # 股票
    FUTURE = "future"  # 期货
    BOND = "bond"  # 债券
    OPTION = "option"  # 期权
    CASH = "cash"  # 现金


class PositionDirection(str, Enum):
    """持仓方向枚举"""

    LONG = "long"  # 多头
    SHORT = "short"  # 空头


class PositionStatus(str, Enum):
    """持仓状态枚举"""

    ACTIVE = "active"  # 活跃
    CLOSED = "closed"  # 已平仓
    SUSPENDED = "suspended"  # 暂停


class Base(DeclarativeBase):
    pass


class BaseDao(Base, MappedAsDataclass):
    """抽象类,所有字段都不需要 init."""

    __abstract__ = True

    __table_args__ = {"mysql_engine": "InnoDB"}
    __mapper_args__ = {"always_refresh": True}
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    # create_time: Mapped[datetime] = mapped_column(
    #     DATETIME,
    #     init=False,
    #     nullable=False,
    #     server_default=text("CURRENT_TIMESTAMP"),
    # )
    # update_time: Mapped[datetime] = mapped_column(
    #     DATETIME,
    #     init=False,
    #     nullable=False,
    #     server_default=text("CURRENT_TIMESTAMP"),
    #     onupdate=datetime.now,
    #     # server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    #     # server_onupdate=text("CURRENT_TIMESTAMP"),
    #     # 这两行无法使用的原因
    #     # 1. server_onupdate = current_timestamp 不生效
    #     # 2. server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP") 仅支持mysql，不支持sqlite
    # )


# 基金实体表
class Fund(BaseDao):
    """基金实体表."""

    __tablename__ = "fund"

    fund_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="基金id")
    fund_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="基金名称")
    fund_code: Mapped[str] = mapped_column(String(255), nullable=False, comment="基金代码")


class FundSnapshotDao(BaseDao):
    """基金快照数据模型."""

    __tablename__ = "fund_snapshot"

    fund_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="基金id")
    fund_asset: Mapped[float] = mapped_column(
        DECIMAL(18, 6), nullable=False, comment="基金产品资产"
    )
    is_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="投资策略id")
    is_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="投资策略名称")
    is_type: Mapped[str] = mapped_column(String(255), nullable=False)
    bsp_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="基准组合id")
    bsp_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="基准组合名称")
    bsp_type: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="stock|future")
    sa_type: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="策略账户类型")
    is_wt: Mapped[float] = mapped_column(Double, nullable=False, comment="投资策略权重")
    bsp_wt: Mapped[float | None] = mapped_column(Double, nullable=True, comment="基准组合权重")
    basis_pos_pct: Mapped[float | None] = mapped_column(Double, nullable=True, comment="基差仓位")
    mv_wt: Mapped[float | None] = mapped_column(Double, nullable=True, comment="目标市值权重")
    bsp_asset: Mapped[float | None] = mapped_column(DECIMAL(18, 6), nullable=True)
    bsp_mv: Mapped[float | None] = mapped_column(Double, nullable=True)
    bsp_share: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="期货手数")
    future_price: Mapped[float | None] = mapped_column(Double, nullable=True, comment="期货价格")
    target_is_expo: Mapped[float | None] = mapped_column(
        Double, nullable=True, comment="目标is expo"
    )
    trading_day: Mapped[date] = mapped_column(
        DATETIME, nullable=False, index=True, comment="交易日"
    )
    updater: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default="", comment="更新者，可作为修改批次号"
    )
