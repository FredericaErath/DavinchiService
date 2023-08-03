import time
from datetime import datetime
from typing import Union

from fastapi import HTTPException

from constant import DC_DEPARTMENT_REVERSE, DC_DEPARTMENT
from core.database import get_surgery, get_user, get_instrument, get_supply


def get_surgery_by_tds(begin_time: datetime = None,
                       end_time: datetime = None,
                       department: Union[str, list[str]] = None,
                       s_name: Union[str, list[str]] = None):
    if department is not None:
        if isinstance(department, str):
            department = DC_DEPARTMENT.get(department)
        elif isinstance(department, list):
            department = list(map(lambda x: DC_DEPARTMENT.get(x), department))
        else:
            raise HTTPException(status_code=400, detail="Invalid department")

    def _format_surgery(x):
        surgeon = get_user(u_id=x["chief_surgeon"])[0]
        x["chief_surgeon"] = surgeon["name"]
        x["chief_surgeon_id"] = surgeon["u_id"]
        associate = get_user(u_id=x["associate_surgeon"])[0]
        x["associate_surgeon"] = associate["name"]
        x["associate_surgeon_id"] = associate["u_id"]
        x["instrument_nurse_detail"] = list(map(lambda y: get_user(u_id=y)[0], x["instrument_nurse"]))
        x["instrument_nurse"] = ', '.join(list(map(lambda y: y["name"], x["instrument_nurse_detail"])))
        x["circulating_nurse_detail"] = list(map(lambda y: get_user(u_id=y)[0], x["circulating_nurse"]))
        x["circulating_nurse"] = ', '.join(list(map(lambda y: y["name"], x["circulating_nurse_detail"])))

        def _get_instrument_detail(y):
            instrument = get_instrument(i_id=y["id"])[0]
            return {"id": instrument["i_id"], "name": instrument["i_name"], "times": instrument["times"],
                    "description": y["description"]}

        x["instruments_detail"] = list(map(lambda y: _get_instrument_detail(y), x["instruments"]))
        x["instruments"] = ', '.join(list(map(lambda y: y["name"], x["instruments_detail"])))
        x["consumables_detail"] = list(map(lambda y: get_supply(c_id=y)[0], x["consumables"]))
        x["consumables"] = ', '.join(list(map(lambda y: y["c_name"], x["consumables_detail"])))
        x["department"] = DC_DEPARTMENT_REVERSE.get(x["department"])
        x["date"] = x["date"].strftime("%Y-%m-%d")
        x["begin_time"] = x["begin_time"].strftime("%H:%M")
        x["end_time"] = x["end_time"].strftime("%H:%M")
        return x

    surgery = get_surgery(begin_time=begin_time, end_time=end_time, department=department, s_name=s_name)
    if len(surgery) == 0:
        return []
    else:
        surgery = list(map(lambda x: _format_surgery(x), surgery))
        return surgery

