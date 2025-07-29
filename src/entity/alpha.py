import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ModelTypeEnum(str, Enum):
    """模型的类别枚举
    不同的模型有不同的输入输出，处理逻辑
    比如 alpha model，输出的是某天某个时间点股票的alpha值，代表股票的预测收益率
    择时模型，输出的是股票的 alpha 值，还有 beta 值
    期货模型，输出的是期货的比例，比如 -0.5 表示开空头， 0.5 表示开多头
    """

    ALPHA = "ALPHA"
    TIMING = "TIMING"
    FUTURES = "FUTURES"


# Benchmark 枚举（基于常见值，成员名为可读形式，值为原始字符串）
class BenchmarkEnum(str, Enum):
    # 中证500
    SSE_000905 = "000905.SSE"  # 最常见，1342 次
    # 沪深300
    SSE_000300 = "000300.SSE"  # 1207 次
    # 中证1000
    SSE_000852 = "000852.SSE"  # 818 次
    # 全市场等权指数
    EQL_000000 = "000000.EQL"  # 146 次
    # 中证2000
    SSE_932000 = "932000.SSE"  # 113 次
    # 双创
    EQL_688300 = "688300.EQL"  # 81 次
    # 天相
    TX_998122 = "998122.TX"  # 58 次
    # 中证800
    SSE_000906 = "000906.SSE"  # 22 次
    # 科创50
    SSE_000688 = "000688.SSE"  # 3 次
    # 25% 科创50 + 25% 科创100 + 50% 科创板指数
    LQI_683088 = "683088.LQI"  # 3 次


# Universe 枚举（基于常见值，成员值为元组形式，空列表用空元组表示）
class UniverseEnum(Enum):
    EMPTY = tuple()  # 最常见，2634 次，相当于 []
    SSE_000300 = ("000300.SSE",)  # 416 次
    SSE_300_905_852 = ("000300.SSE", "000905.SSE", "000852.SSE")  # 247 次
    NON_KECHUANG = ("非科创板",)  # 245 次
    SSE_300_905 = ("000300.SSE", "000905.SSE")  # 139 次
    SSE_000852 = ("000852.SSE",)  # 38 次
    STOCKDIV_TOP500 = ("922_stockdiv_top500",)  # 27 次
    ZZ800 = ("zz800",)  # 10 次
    SSE_000905 = ("000905.SSE",)  # 2 次
    CHUANGYE_KECHUANG = ("创业板", "科创板")  # 1 次
    # 可以添加更多，如 NON_CHUANGYE = ("非创业板",)


class ConstraintModel(BaseModel):
    benchmark: BenchmarkEnum = Field(..., description="基准指数枚举，例如 BenchmarkEnum.SSE_000905")
    universe: UniverseEnum = Field(
        default=UniverseEnum.EMPTY, description="股票池枚举，例如 UniverseEnum.SSE_000300"
    )
    max_weight: float = Field(..., description="单股最大权重，例如 0.005")
    weight_bias: list[float] = Field(default=[], description="权重偏差范围，例如 [-0.02, 0.02]")
    turnover_rate: float = Field(..., description="目标换手率，例如 0.2")
    risk_aversion: int = Field(default=0, description="风险厌恶系数，例如 500")
    industry_up_limit: float = Field(default=0.05, description="行业暴露上限，例如 0.05")
    industry_down_limit: float = Field(default=-0.05, description="行业暴露下限，例如 -0.05")

    class Config:
        str_strip_whitespace = True  # 自动去除字符串空白
        validate_assignment = True  # 启用赋值验证


class StrategySchedule(BaseModel):
    """策略调度"""

    times: list[datetime.time] = Field(
        ..., description="调度时间，例如 [time.time(9, 30), time.time(14, 30)]"
    )


class BaseAlphaStrategy(BaseModel):
    """基准 alpha 策略
    包含一个 alpha model 和 一组约束条件
    """

    alpha_name: str
    constraints: ConstraintModel
