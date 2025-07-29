import datetime
import os

os.environ["VIRGO_DATA_SERVER_HOST"] = "d13.sci-inv.cn"
import pandas as pd
import virgo

virgo.init("virgo", "xYu6H4VUaltcEZgi")


def get_alpha(
    alpha_name: str, alpha_time: str, *, date: datetime.date, intraday: bool = False
) -> pd.DataFrame:
    return virgo.table.read(
        f"alpha.{alpha_name}",
        date=str(date),
        partitions={"alpha_time": alpha_time},
        intraday=intraday,
    )


if __name__ == "__main__":
    print(get_alpha("mars_v8", "10:00", date=datetime.date(2025, 7, 28), intraday=True))

    print(virgo.stock.snapshots("ALL", "2025-07-28", "2025-07-28", "10:00:00", "10:00:00"))
