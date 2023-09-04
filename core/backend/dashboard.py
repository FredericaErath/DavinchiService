from datetime import datetime
import pandas as pd

from core.backend.surgery import get_surgery_by_tds


def get_detail_count(df, name: str):
    """Helper function to get instrument or consumables time series info"""

    def _get_instrument(x):
        dict_x = x[f"{name}_detail"]
        dict_x["date"] = x["date"][0:7]
        return dict_x

    df = df[[f"{name}_detail", "date"]].explode(f"{name}_detail")
    df[f"{name}_detail"] = df.apply(lambda x: _get_instrument(x), axis=1)
    df = pd.DataFrame(df[f"{name}_detail"].tolist())
    if name == "instruments":
        group_by_key = ["date", "id"]
    else:
        group_by_key = ["date", "name"]
    count = df.groupby(group_by_key).count()["description"].reset_index().rename(
        columns={"description": "count"})
    count = count.merge(
        df[["id", "name", "description", "date"]],
        on=group_by_key, validate="m:m", how="left").drop_duplicates(subset=group_by_key).sort_values(["name", "id"])

    accident_count = df[df["description"] != "默认"]
    if len(accident_count) != 0:
        accident_group = accident_count.groupby(group_by_key).count()[
            "description"].reset_index().rename(
            columns={"description": "count"})
        accident_count = accident_count[["id", "name", "description", "date"]].merge(
            accident_group,
            on=group_by_key, validate="m:m", how="left").sort_values(["name", "id"])
    else:
        accident_count = []
    return count, accident_count


def get_surgery_dashboard(begin_time: datetime = None, end_time: datetime = None):
    df = pd.DataFrame(get_surgery_by_tds(begin_time=begin_time, end_time=end_time))
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

    # get count
    instrument_count, accident_instrument_count = get_detail_count(df, "instruments")
    consumable_count, accident_consumable_count = get_detail_count(df, "consumables")

    # get time series
    instrument_time_series = get_time_series(instrument_count, "instruments")
    instrument_accident_time_series = get_time_series(accident_instrument_count, "instruments")

    return {"df": df[["chief_surgeon", "date", "p_name"]].to_dict('records'),
            "surgeon_count": surgeon_count.to_dict('records'),
            "nurse_count": df_nurse.to_dict('records'), "department_count": department_count.to_dict('records'),
            "top_ten": [df_top_ten["c_count"].tolist(), df_top_ten["chief_surgeon"].tolist()],
            "instrument_count": instrument_count.to_dict('records'),
            "accident_instrument_count": accident_instrument_count.to_dict('records'),
            "consumable_count": consumable_count.to_dict('records'),
            "accident_consumable_count": accident_consumable_count.to_dict('records'),
            "instrument_time_series": instrument_time_series,
            "instrument_acc_time_series": instrument_accident_time_series}


def get_doctor_contribution(df: list, name: str):
    df = pd.DataFrame(df)
    df = df[df["chief_surgeon"] == name].groupby(["date"]).count()["p_name"].reset_index().rename(
        columns={"p_name": "count"})
    return df.to_dict("records")


def get_time_series(df, name: str):
    x_axis = df["date"].drop_duplicates().sort_values()
    series = df[["name", "count", "date", "id"]]
    data = []
    legend = []
    for key, value in series.groupby(["id"]):
        value = value.merge(x_axis, on="date", how="outer").sort_values("date").fillna(0)
        name = f"{key[0]}号{value['name'][0]}"
        legend.append(name)
        data.append({"name": name, "data": value["count"].tolist(), "type": "line"})
    return {"xAxis": x_axis.tolist(), "series": data, "legend": legend}
