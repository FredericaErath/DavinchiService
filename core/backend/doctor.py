"""
Doctor end operations
"""
import pandas as pd
from fastapi import HTTPException
from core.database import get_surgery


def general_statistics(u_id: str):
    """General purposed statistics."""
    surgeries = get_surgery(chief_surgeon=u_id)
    if len(surgeries) == 0:
        raise HTTPException(status_code=400, detail="The user do not had any surgery records yet.")
    df = pd.DataFrame(surgeries)
    df["hours"] = df["end_time"] - df["begin_time"]
    df["count_instruments"] = df.apply(lambda x: len(x["instruments"]), axis=1)
    df["count_consumables"] = df.apply(lambda x: len(x["consumables"]), axis=1)
    return {"num_surgery": len(df), "total_instruments": df["count_instruments"].sum(),
            "total_consumables": df["count_consumables"].sum(), "total_hours": str(df["hours"].sum())}


def surgery_by_type(u_id: str):
    """Counted by type of surgery performed by doctors."""
    surgeries = get_surgery(chief_surgeon=u_id)
    if len(surgeries) == 0:
        raise HTTPException(status_code=400, detail="The user do not had any surgery records yet.")
    df = pd.DataFrame(surgeries).groupby("s_name").count().reset_index()[["s_name", "p_name"]]
    res = df.rename(columns={"p_name": "value", "s_name": "name"}).to_dict('records')
    return res


def surgery_by_time(u_id: str):
    """Time series of surgeries."""
    surgeries = get_surgery(chief_surgeon=u_id)
    if len(surgeries) == 0:
        raise HTTPException(status_code=400, detail="The user do not had any surgery records yet.")
    df = pd.DataFrame(surgeries).groupby("date").count().reset_index()[["p_name", "date"]]
    res = df.rename(columns={"p_name": "value", "date": "name"}).to_dict('records')
    return res
