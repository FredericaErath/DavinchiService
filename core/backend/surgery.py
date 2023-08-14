import time
from collections import Counter
from datetime import datetime
from typing import Union

from fastapi import HTTPException

from constant import DC_DEPARTMENT_REVERSE, DC_DEPARTMENT
from core.backend.instrument import revise_instrument
from core.backend.supply import update_supply_description
from core.database import get_surgery, get_user, get_instrument, get_supply, update_surgery, insert_surgery


def get_surgery_by_tds(page: int = None,
                       limit_size: int = None,
                       begin_time: datetime = None,
                       end_time: datetime = None,
                       department: Union[str, list[str]] = None,
                       s_name: Union[str, list[str]] = None):
    """
    This get function should support pagination.
    """
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
        x["instrument_nurse"] = ','.join(list(map(lambda y: y["name"], x["instrument_nurse_detail"])))
        x["circulating_nurse_detail"] = list(map(lambda y: get_user(u_id=y)[0], x["circulating_nurse"]))
        x["circulating_nurse"] = ','.join(list(map(lambda y: y["name"], x["circulating_nurse_detail"])))

        def _get_instrument_detail(y):
            instrument = get_instrument(i_id=y["id"])[0]
            return {"id": instrument["i_id"], "name": instrument["i_name"], "times": instrument["times"],
                    "description": y["description"]}

        def _get_consumable_detail(y):
            consumable = get_supply(c_id=y)[0]
            return {"id": consumable["c_id"], "name": consumable["c_name"],
                    "description": consumable["description"]}

        x["instruments_detail"] = list(map(lambda y: _get_instrument_detail(y), x["instruments"]))
        x["instruments"] = ','.join(list(map(lambda y: y["name"], x["instruments_detail"])))
        x["consumables_detail"] = list(map(lambda y: _get_consumable_detail(y), x["consumables"]))
        x["consumables"] = ','.join(list(map(lambda y: y["name"], x["consumables_detail"])))
        x["department"] = DC_DEPARTMENT_REVERSE.get(x["department"])
        x["date"] = x["date"].strftime("%Y-%m-%d")
        x["begin_time"] = x["begin_time"].strftime("%H:%M")
        x["end_time"] = x["end_time"].strftime("%H:%M")
        return x

    if page is not None and limit_size is not None:
        skip_size = (page - 1) * limit_size
    else:
        skip_size = None
    surgery = get_surgery(skip_size=skip_size, limit_size=limit_size,
                          begin_time=begin_time, end_time=end_time, department=department, s_name=s_name)
    if len(surgery) == 0:
        return []
    else:
        surgery = list(map(lambda x: _format_surgery(x), surgery))
        return surgery


def update_surgery_info(s_id: int,
                        p_name: str = None,
                        begin_time: datetime = None,
                        end_time: datetime = None,
                        date: datetime = None,
                        admission_number: int = None,
                        department: Union[str, list[str]] = None,
                        s_name: Union[str, list[str]] = None,
                        chief_surgeon: Union[str, list[str]] = None,
                        associate_surgeon: Union[str, list[str]] = None,
                        instrument_nurse: list[str] = None,
                        circulating_nurse: list[str] = None,
                        instruments: list = None,
                        consumables: list = None):
    # format every input parameter
    if department is not None:
        department = DC_DEPARTMENT.get(department)

    if instruments is not None:
        def _revise_instruments(x):
            revise_instrument(x["id"], x["times"])
            return {"id": x["id"], "description": x["description"]}

        instruments = list(map(lambda x: _revise_instruments(x), instruments))

    if consumables is not None:
        def _revise_consumables(x):
            update_supply_description(x["id"], x["description"])
            return x["id"]

        consumables = list(map(lambda x: _revise_consumables(x), consumables))

    res = update_surgery(s_id=s_id, begin_time=begin_time, date=date, admission_number=admission_number,
                         end_time=end_time, department=department, s_name=s_name, p_name=p_name,
                         chief_surgeon=chief_surgeon, associate_surgeon=associate_surgeon,
                         instrument_nurse=instrument_nurse, circulating_nurse=circulating_nurse,
                         instruments=instruments, consumables=consumables)

    if res == "unsuccessful":
        raise HTTPException(status_code=400, detail="Update failed. Please check the input info.")
    else:
        return res


def insert_surgery_admin(begin_time: datetime,
                         end_time: datetime,
                         p_name: str,
                         date: datetime,
                         admission_number: int,
                         department: str,
                         s_name: str,
                         chief_surgeon: str,
                         associate_surgeon: str,
                         instrument_nurse: list[str],
                         circulating_nurse: list[str],
                         instruments: list[dict],
                         consumables: list[int]):
    # format every input parameter
    if department is not None:
        department = DC_DEPARTMENT.get(department)

    if instruments is not None:
        def _revise_instruments(x):
            revise_instrument(x["id"], x["times"]-1)
            return {"id": x["id"], "description": x["description"]}

        instruments = list(map(lambda x: _revise_instruments(x), instruments))

    if consumables is not None:
        def _revise_consumables(x):
            update_supply_description(x["id"], x["description"])
            return x["id"]

        consumables = list(map(lambda x: _revise_consumables(x), consumables))

    res = insert_surgery(begin_time=begin_time, date=date, admission_number=admission_number,
                         end_time=end_time, department=department, s_name=s_name, p_name=p_name,
                         chief_surgeon=chief_surgeon, associate_surgeon=associate_surgeon,
                         instrument_nurse=instrument_nurse, circulating_nurse=circulating_nurse,
                         instruments=instruments, consumables=consumables)

    if res == "unsuccessful":
        raise HTTPException(status_code=400, detail="Insert failed. Please check the input info.")
    else:
        return res
