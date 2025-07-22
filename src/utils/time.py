from datetime import datetime, timedelta


def _trade_time_add_optimized(cur_time: str, add_min: int) -> str:
    """
    优化的交易时间加法函数
    处理股市交易时间：上午 9:30-11:30，下午 13:00-15:00

    Args:
        cur_time: 当前时间字符串，格式 "HH:MM:SS"
        add_min: 要增加的分钟数

    Returns:
        计算后的时间字符串，格式 "HH:MM:SS"
    """
    # 解析时间
    hour, minute, second = map(int, cur_time.split(":"))

    # 转换为分钟表示，便于计算
    current_minutes = hour * 60 + minute
    target_minutes = current_minutes + add_min

    # 检查是否跨越午休时间 (11:30 = 690分钟)
    morning_end = 11 * 60 + 30  # 11:30
    afternoon_start = 13 * 60  # 13:00
    afternoon_end = 14 * 60 + 57  # 14:57

    # 如果当前在上午时段，目标时间超过11:30，则跳到下午
    if current_minutes < morning_end and target_minutes > morning_end:
        # 计算超出11:30的时间，加到下午13:00开始
        overflow_minutes = target_minutes - morning_end
        target_minutes = afternoon_start + overflow_minutes

    # 限制最大时间不超过14:57
    if target_minutes > afternoon_end:
        target_minutes = afternoon_end
        second = 0  # 重置秒数

    # 转换回时分秒格式
    target_hour = target_minutes // 60
    target_minute = target_minutes % 60

    return f"{target_hour:02d}:{target_minute:02d}:{second:02d}"


def _trade_time_add_elegant(cur_time: str, add_min: int) -> str:
    """
    最优雅的实现：使用datetime处理，精确处理午休时间

    Args:
        cur_time: 当前时间字符串，格式 "HH:MM:SS"
        add_min: 要增加的分钟数

    Returns:
        计算后的时间字符串，格式 "HH:MM:SS"
    """
    # 定义交易时间段
    MORNING_END = datetime(2023, 1, 1, 11, 30, 0)
    AFTERNOON_START = datetime(2023, 1, 1, 13, 0, 0)
    TRADING_END = datetime(2023, 1, 1, 14, 57, 0)
    LUNCH_BREAK_DURATION = 90  # 午休90分钟

    # 解析当前时间
    hour, minute, second = map(int, cur_time.split(":"))
    current_time = datetime(2023, 1, 1, hour, minute, second)

    # 简单加法
    target_time = current_time + timedelta(minutes=add_min)

    # 处理跨越午休的情况
    if current_time < MORNING_END and target_time > MORNING_END:
        # 跨越午休，需要加上午休时间
        target_time += timedelta(minutes=LUNCH_BREAK_DURATION)

    # 限制在交易时间内
    target_time = min(target_time, TRADING_END)

    return target_time.strftime("%H:%M:%S")


def _trade_time_add_v2(cur_time: str, add_min: int) -> str:
    """
    修正版本：精确处理午休时间（1.5小时）

    Args:
        cur_time: 当前时间字符串，格式 "HH:MM:SS"
        add_min: 要增加的分钟数

    Returns:
        计算后的时间字符串，格式 "HH:MM:SS"
    """
    hour, minute, second = map(int, cur_time.split(":"))

    # 创建datetime对象便于时间计算
    base_date = datetime(2023, 1, 1, hour, minute, second)
    target_time = base_date + timedelta(minutes=add_min)

    # 检查是否跨越11:30
    morning_cutoff = datetime(2023, 1, 1, 11, 30, 0)
    if base_date < morning_cutoff and target_time > morning_cutoff:
        # 跨越午休，加上午休时间1.5小时（90分钟）
        target_time += timedelta(minutes=90)

    # 限制最大时间14:57
    max_time = datetime(2023, 1, 1, 14, 57, 0)
    if target_time > max_time:
        target_time = max_time

    return target_time.strftime("%H:%M:%S")


# 原始函数（保留作为对比）
def _trade_time_add_original(cur_time, add_min):
    """原始实现"""
    arr = cur_time.split(":")
    cur_h = int(arr[0])
    cur_m = int(arr[1])
    cur_s = int(arr[2])
    dst_m = cur_m + add_min
    dst_h = cur_h + int(dst_m / 60)
    dst_m = int(dst_m % 60)
    dst_s = cur_s
    dst_hm = dst_h * 100 + dst_m
    cur_hm = cur_h * 100 + cur_m
    if cur_hm < 1130 and dst_hm > 1130:
        d_h = max(dst_h - 11, 0)
        d_m = d_h * 60 + dst_m - 30
        dst_h = 13 + int(d_m / 60)
        dst_m = int(d_m % 60)
    dst_hm = dst_h * 100 + dst_m
    if dst_hm > 1457:
        dst_h = 14
        dst_m = 57
        dst_s = 0
    return "%02d:%02d:%02d" % (dst_h, dst_m, dst_s)


# 测试函数
def test_trade_time_functions():
    """测试不同实现的一致性"""
    test_cases = [
        ("10:30:15", 30),  # 正常上午时间
        ("11:00:00", 45),  # 跨越午休
        ("13:30:00", 60),  # 下午时间
        ("14:30:00", 60),  # 超过下午结束时间
        ("09:30:00", 180),  # 大幅跨越
    ]

    print("测试结果对比:")
    print("时间输入 | 增加分钟 | 原始实现 | 优化实现1 | 优雅实现 | 修正实现")
    print("-" * 70)

    for time_str, minutes in test_cases:
        original = _trade_time_add_original(time_str, minutes)
        optimized1 = _trade_time_add_optimized(time_str, minutes)
        elegant = _trade_time_add_elegant(time_str, minutes)
        fixed_v2 = _trade_time_add_v2(time_str, minutes)

        print(
            f"{time_str} | +{minutes:3d}分钟 | {original} | {optimized1} | {elegant} | {fixed_v2}"
        )


if __name__ == "__main__":
    test_trade_time_functions()
