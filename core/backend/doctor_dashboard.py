from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta

from core.database import get_surgery, get_user, get_instrument, get_supply


def get_general_data_by_month(surgeon_id: str, begin_time: datetime = None, end_time: datetime = None):
    if begin_time is None and end_time is None:
        # this month by default
        end_time = datetime.now()
        begin_time = end_time - relativedelta(month=1)
    surgery = get_surgery(chief_surgeon=surgeon_id, begin_time=begin_time, end_time=end_time)
    df = pd.DataFrame(surgery)[["s_id", "date", "begin_time", "end_time", "instruments", "consumables", "s_name"]]
    df["instrument_count"] = df.apply(lambda x: len(x["instruments"]), axis=1)
    df["consumable_count"] = df.apply(lambda x: len(x["consumables"]), axis=1)
    sur_count, ins_count, con_count = len(df), df["instrument_count"].sum(), df["consumable_count"].sum()

    # get type percentage
    surgery_type_count = df.groupby("s_name").count()["s_id"].reset_index().rename(columns={"s_name": "name",
                                                                                            "s_id": "value"})
    surgery_type_count["value"] = surgery_type_count["value"]
    df_ins = df.explode("instruments").reset_index(drop=True)[["s_id", "instruments", "instrument_count"]]
    df_con = df.explode("consumables").reset_index(drop=True)[["s_id", "consumables", "consumable_count"]]

    def _get_instrument_type(x):
        x["instruments"] = get_instrument(i_id=x["instruments"]["id"])[0]["i_name"]
        return x

    def _get_consumable_type(x):
        x["consumables"] = get_supply(c_id=x["consumables"])[0]["c_name"]
        return x

    df_ins = df_ins.apply(lambda x: _get_instrument_type(x), axis=1)
    df_con = df_con.apply(lambda x: _get_consumable_type(x), axis=1)
    df_ins_count = df_ins.groupby("instruments").count()["s_id"].reset_index().rename(columns={"instruments": "name",
                                                                                               "s_id": "value"})
    df_con_count = df_con.groupby("consumables").count()["s_id"].reset_index().rename(columns={"consumables": "name",
                                                                                               "s_id": "value"})
    df_ins_count["value"] = df_ins_count["value"]
    df_con_count["value"] = df_con_count["value"]

    return {"surgery_count": sur_count, "instrument_count": ins_count, "consumables_count": con_count,
            "ins_detail_count": df_ins_count.to_dict('records'), "con_detail_count": df_con_count.to_dict('records'),
            "sur_detail_count": surgery_type_count.to_dict('records')}


def get_surgery_time_series(surgeon_id: str, mode: str = None):
    """
    Get surgery, instrument, consumables time series.

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
    sur_percent = (len_users - surgery_rank) / len_users
    ins_percent = (len_users - instrument_rank) / len_users
    con_percent = (len_users - consumable_rank) / len_users
    df = df[df["chief_surgeon"] == surgeon_id]
    df["duration"] = df.apply(lambda x: x["end_time"] - x["begin_time"], axis=1)
    df = df.groupby("s_name")["duration"].sum().reset_index()
    return {"sur_percent": sur_percent, "ins_percent": ins_percent,
            "con_percent": con_percent, "duration": df.to_dict("records")}
