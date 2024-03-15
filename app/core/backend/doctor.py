"""
Doctor end operations
"""
from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from fastapi import HTTPException

from core.database import get_surgery, get_user, get_instrument, get_supply
from app.core.database.message import insert_message, get_message


def get_general_data_by_month(surgeon_id: str, begin_time: datetime = None, end_time: datetime = None):
    if begin_time is None and end_time is None:
        # this month by default
        end_time = datetime.now()
        begin_time = end_time - relativedelta(month=1)
    surgery = get_surgery(chief_surgeon=surgeon_id, begin_time=begin_time, end_time=end_time)
    df = pd.DataFrame(surgery)[["s_id", "date", "begin_time", "end_time", "instruments", "consumables", "s_name"]]
    if len(df) == 0:
        return {"surgery_count": 0, "instrument_count": 0, "consumables_count": 0,
                "ins_detail_count": [],
                "con_detail_count": [],
                "sur_detail_count": []}
    else:
        df = df[["s_id", "date", "begin_time", "end_time", "instruments", "consumables", "s_name"]]
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

        return {"surgery_count": int(sur_count), "instrument_count": int(ins_count), "consumables_count": int(con_count),
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

        return {"category": surgery_count["time"].tolist(), "data": surgery_count["s_count"].tolist()}
    else:
        return []


def get_contribution_matrix(surgeon_id):
    """Turn doctor's contribution into a 7*10 matrix"""
    # get begin_time and end_time
    end_time = datetime.now()
    month = end_time.strftime('%Y年%m月')
    weekday = (end_time.weekday() + 1) % 7
    begin_time = end_time - relativedelta(days=weekday + 63)

    # get surgery count
    df = pd.DataFrame(get_surgery(chief_surgeon=surgeon_id, begin_time=begin_time, end_time=end_time))
    if len(df) == 0:
        matrix = [[0]*10 for _ in range(10)]
        hours = 0
    else:
        df = df[["s_id", "date"]]
        df_month = pd.DataFrame(get_surgery(chief_surgeon=surgeon_id, end_time=end_time,
                                            begin_time=end_time.replace(day=1, hour=0, minute=0, second=0)))

        if len(df_month) == 0:
            hours = 0
        else:
            df_month = df_month[["s_id", "begin_time", "end_time"]]
            df_month["hours"] = df_month["end_time"] - df_month["begin_time"]
            hours = df_month["hours"].sum().seconds/3600

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
                matrix[i] = list(map(lambda x: [int(x)], df_time[i * 7: (i + 1) * 7].tolist()))
            else:
                # the last week
                matrix[i] = list(map(lambda x: [int(x)],
                                     df_time[i * 7:].tolist())) + list(map(lambda x: [int(x)], matrix[i][weekday - 7 + 1:]))
    return {"matrix": matrix, "month": month, "hours": "%.1f" % hours}


def get_surgery_by_date(surgeon_id: str, date: datetime = None):
    """Get surgery rank detail by date."""
    if not date:
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    len_users = len(get_user(user_type="医生"))
    df = pd.DataFrame(get_surgery(date=date))
    if len(df) == 0:
        return {"sur_percent": 0, "ins_percent": 0,
                "con_percent": 0, "duration": [df.to_dict("records")]}
    else:
        df = df[["s_id", "s_name", "chief_surgeon", "instruments", "consumables", "begin_time", "end_time"]]
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
        df["duration"] = df.apply(lambda x: int((x["end_time"] - x["begin_time"]).total_seconds() / 3600), axis=1)
        df = df.groupby("s_name")["duration"].sum().reset_index().reset_index()
        dur_sum = int(df["duration"].sum())
        pre = 0

        def _get_dur_ls(x):
            nonlocal pre
            ls = [None] * dur_sum
            duration = x["duration"]
            ls[pre: pre + duration] = [0] * duration
            pre += duration
            return ls

        df["duration"] = df.apply(lambda x: _get_dur_ls(x), axis=1)
        df.rename(columns={"s_name": "name", "duration": "data"}, inplace=True)

        return {"sur_percent": sur_percent, "ins_percent": ins_percent, "con_percent": con_percent,
                "series": df[["name", "data"]].to_dict('records'), "categories": list(range(dur_sum)), "len": dur_sum}


def send_message(u_id: str, u_name: str, message: str):
    res = insert_message(u_id=u_id, u_name=u_name, content=message)
    if res == "unsuccessful":
        raise HTTPException(status_code=400, detail="Insert failure, please check your info.")
    else:
        return res


def get_message_by_uid(u_id: str):
    """
    Get message sent from user.
    """
    res = get_message(u_id=u_id)
    if len(res) == 0:
        return []
    else:
        def _format_message(x):
            x["status"] = x["status"]-1
            x["insert_time"] = x["insert_time"].strftime("%Y-%m-%d %H:%M:%S")
            return x
        res = list(map(lambda x: _format_message(x), res))
        return res
