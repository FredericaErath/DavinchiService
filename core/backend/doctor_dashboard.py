from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta

from core.database import get_surgery


def get_surgery_by_surgeon(surgeon_id: str, begin_time: datetime = None, end_time: datetime = None):
    """Get surgery by surgeon."""
    if begin_time is None and end_time is None:
        # this month by default
        end_time = datetime.now()
        begin_time = end_time - relativedelta(month=1)
    surgery = get_surgery(chief_surgeon=surgeon_id, begin_time=begin_time, end_time=end_time)
    return surgery


def get_general_data_by_month(surgery: dict):
    df = pd.DataFrame(surgery)[["s_id", "date", "begin_time", "end_time", "instruments", "consumables"]]
    df["instrument_count"] = df.apply(lambda x: len(x["instruments"]), axis=1)
    df["consumable_count"] = df.apply(lambda x: len(x["consumables"]), axis=1)
    return {"surgery_count": len(df),
            "instrument_count": df["instrument_count"].sum(), "consumables_count": df["consumable_count"].sum()}


def get_surgery_time_series(surgeon_id: str, mode: str = None, ):
    """
    Get surgery time series.
    :param surgeon_id: surgeon's user id
    :param mode: Year, month or day, year by default.
    :return: dict of time series
    """
    if mode is None:
        mode = "year"
    if mode == "year":
        begin_time, end_time = None, None
    elif mode == "month":
        # look back 9 months
        end_time = datetime.now()
        begin_time = end_time - relativedelta(months=9)
    else:
        # look back 7 days
        end_time = datetime.now()
        begin_time = end_time - relativedelta(days=7)

    surgery = get_surgery(chief_surgeon=surgeon_id, begin_time=begin_time, end_time=end_time)
    if surgery:
        df = pd.DataFrame(surgery)[["s_id", "date", "begin_time", "end_time"]]
        if mode == "year":
            df["time"] = df["date"].dt.year
        elif mode == "month":
            df["time"] = df["date"].dt.strftime('%Y-%m')
        else:
            df["time"] = df["date"].dt.date

        surgery_count = df.groupby("time").count()["s_id"].reset_index().rename(columns={"s_id": "s_count"})
        return surgery_count.to_dict('records')
    else:
        return []

