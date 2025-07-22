import time

import polars as pl
from sqlalchemy import select

from src.db.database import get_db_session
from src.db.models import FundSnapshotDao


def time_cost(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Time cost: {end_time - start_time} seconds")
        return result

    return wrapper


@time_cost
def test_read():
    with get_db_session() as session:
        stmt = select(FundSnapshotDao)
        result = session.execute(stmt).scalars().all()
        print(result[0])
        df = pl.DataFrame(result)
        print(df)


if __name__ == "__main__":
    test_read()
