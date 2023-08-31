from datetime import datetime
import pandas as pd

from core.backend.surgery import get_surgery_by_tds


def get_surgery_dashboard(begin_time: datetime = None, end_time: datetime = None):
    df = pd.DataFrame(get_surgery_by_tds(begin_time=begin_time, end_time=end_time))
    print(df)
    if len(df) == 0:
        return {"surgeon_count": [], "nurse_count": [], "department_count": [], "top_ten": [[], []]}
    # get surgeon and department count
    surgeon_count = df.groupby(["department",
                                "chief_surgeon"]).count()["p_name"].reset_index().rename(columns={"p_name": "c_count"})
    grouped = surgeon_count.groupby(["department"])["c_count"].sum().reset_index().rename(
        columns={"c_count": "d_count"})
    surgeon_count = surgeon_count.merge(grouped, how="left", on="department", validate="m:1")

    department_count = surgeon_count[["department", "d_count"]].drop_duplicates().rename(
        columns={"department": "name", "d_count": "value"})

    # get nurse count
    df_instrument = df.apply(lambda x: x["instrument_nurse"].split(','), axis=1).explode().reset_index()
    df_circulate = df.apply(lambda x: x["circulating_nurse"].split(','), axis=1).explode().reset_index()
    df_circulate = df_circulate.groupby([0]).count()["index"].reset_index().rename(
        columns={0: "name", "index": "count"})
    df_instrument = df_instrument.groupby([0]).count()["index"].reset_index().rename(
        columns={0: "name", "index": "count"})
    df_nurse = df_circulate.merge(df_instrument, how="outer", on="name", validate="1:1").fillna(0).rename(
        columns={"count_x": "count_circulate", "count_y": "count_instrument"})
    df_nurse["sum"] = df_nurse["count_circulate"] + df_nurse["count_instrument"]

    # get top 10 surgeon
    if len(df) < 10:
        df_top_ten = surgeon_count.sort_values("c_count")[["chief_surgeon", "c_count"]]
    else:
        df_top_ten = surgeon_count.sort_values("c_count")[["chief_surgeon", "c_count"]][:10]

    # get instrument count
    instrument_df = df[["instruments_detail", "date"]].explode("instruments_detail")

    def _get_instrument(x):
        dict_x = x["instruments_detail"]
        dict_x["date"] = x["date"][0:7]
        return dict_x

    instrument_df["instruments_detail"] = instrument_df.apply(lambda x: _get_instrument(x), axis=1)
    instrument_df = pd.DataFrame(instrument_df["instruments_detail"].tolist())
    instrument_count = instrument_df.groupby(["date", "id"]).count()["description"].reset_index().rename(
        columns={"description": "count"})
    instrument_count = instrument_count.merge(
        instrument_df[["id", "name", "description"]],
        on="id", validate="m:m", how="left").drop_duplicates(subset=["id", "date"]).sort_values(["name", "id"])

    # print(instrument_count)
    return {"df": df.to_dict('records'), "surgeon_count": surgeon_count.to_dict('records'),
            "nurse_count": df_nurse.to_dict('records'), "department_count": department_count.to_dict('records'),
            "top_ten": [df_top_ten["c_count"].tolist(), df_top_ten["chief_surgeon"].tolist()],
            "instrument_count": instrument_count.to_dict('records')}


def get_doctor_contribution(df: list, name: str):
    df = pd.DataFrame(df)
    df = df[df["chief_surgeon"] == name].groupby(["date"]).count()["p_name"].reset_index().rename(
        columns={"p_name": "count"})
    return df.to_dict("records")
