from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta

from core.database import get_surgery, get_user

pd.set_option("display.max_columns", None)

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


def get_contribution_matrix(surgeon_id):
    """Turn doctor's contribution into a 7*10 matrix"""
    # get begin_time and end_time
    end_time = datetime.now()
    weekday = end_time.weekday() + 1
    begin_time = end_time - relativedelta(days=weekday + 63)

    # get surgery count
    df = pd.DataFrame(get_surgery(chief_surgeon=surgeon_id, begin_time=begin_time, end_time=end_time))[["s_id", "date"]]
    end_time = end_time.strftime('%Y%m%d')
    begin_time = begin_time.strftime('%Y%m%d')
    df = df.groupby("date").count().reset_index().rename(columns={"s_id": "s_count"})
    df["date"] = df["date"].dt.strftime('%Y-%m-%d')

    # initialize matrix
    matrix = [[0] * 7 for _ in range(10)]
    dates = pd.date_range(begin_time, end_time, freq='1D')
    df_time = pd.DataFrame(dates).rename(columns={0: "date"})
    df_time["date"] = df_time["date"].dt.strftime('%Y-%m-%d')
    # merge
    df_time = df_time.merge(df, on="date", how="left", validate="1:1").fillna(value=0)
    df_time = df_time["s_count"].values

    # fill the matrix
    for i in range(10):
        if i < 9:
            matrix[i] = list(map(int, df_time[i * 7: (i + 1) * 7].tolist()))
        else:
            # the last week
            matrix[i] = list(map(int, df_time[i * 7:].tolist())) + matrix[i][weekday - 7 + 1:]
    return matrix


def get_surgery_by_date(surgeon_id: str, date: datetime):
    """Get surgery rank detail by date."""
    len_users = len(get_user(user_type="医生"))
    df = pd.DataFrame(get_surgery(date=date))[["s_id", "s_name", "chief_surgeon", "instruments", "consumables",
                                               "begin_time", "end_time"]]
    df["instruments"] = df["instruments"].apply(lambda x: len(x))
    df["consumables"] = df["consumables"].apply(lambda x: len(x))
    df_surgery_count = df.groupby("chief_surgeon").count().rename(
        columns={"s_id": "s_count"})[["s_count"]].rank(method="min").reset_index()
    surgery_rank = df_surgery_count[
                          df_surgery_count["chief_surgeon"] == surgeon_id].reset_index()["s_count"][0]
    instrument_count = df.groupby("chief_surgeon")["instruments"].sum().rank(method="min").reset_index()
    instrument_rank = instrument_count[
                          instrument_count["chief_surgeon"] == surgeon_id].reset_index()["instruments"][0]
    consumables_count = df.groupby("chief_surgeon")["consumables"].sum().rank(method="min").reset_index()
    consumable_rank = consumables_count[
                          consumables_count["chief_surgeon"] == surgeon_id].reset_index()["consumables"][
                          0]
    sur_percent = (len_users-surgery_rank)/len_users
    ins_percent = (len_users-instrument_rank)/len_users
    con_percent = (len_users-consumable_rank)/len_users
    df = df[df["chief_surgeon"] == surgeon_id]
    df["duration"] = df.apply(lambda x: x["end_time"] - x["begin_time"], axis=1)
    df = df.groupby("s_name")["duration"].sum().reset_index()
    return {"sur_percent": sur_percent, "ins_percent": ins_percent,
            "con_percent": con_percent, "duration": df.to_dict("records")}


get_surgery_by_date("woshiyisheng", datetime(2023, 8, 29))
