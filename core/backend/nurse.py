"""
Nurse end operations
"""
import logging
import os.path
from datetime import datetime
import json
from typing import Union

import pandas as pd
from fastapi import HTTPException

from constant import BASE_CORE_DIR
from core.database import get_instrument, update_instrument, insert_surgery, update_supply, get_supply, \
    get_newest_supply, get_user

log = logging.getLogger(__name__)


def update_instrument_times_info(i_id: int) -> dict:
    """
    Update instrument times info and return status message

    :param i_id: instrument id
    :return: instrument's status message and times
    """
    instrument = get_instrument(i_id=i_id)[0]
    times = instrument["times"]
    if times > 0:
        times = times - 1
        if update_instrument(v_times=times, i_id=i_id) == "success":
            instrument.update({'times': times})
            return {"msg": "successfully updated instrument times info", "instrument": instrument}
        else:
            return {"msg": "something went wrong when updating instrument info", "instrument": instrument}
    else:
        return {"msg": "The instrument is dumped", "instrument": instrument}


def get_consumable_ls(instruments: list) -> list:
    """
    Get consumable list.

    :param instruments: list of used instrument
    :return: list of consumables
    """
    ls_consumables = ["密封件", "无菌壁套", "中心柱无菌套"]
    if "电剪" in instruments:
        ls_consumables += ["尖端盖附件"]
    return ls_consumables


def get_surgery_names():
    """
    Get surgery list.

    :return: list of surgeries
    """
    dc_surgery_instrument = json.load(open('F:/DavinciService/core/data/surgery_to_instruments.json', encoding='utf-8'))
    return list(dc_surgery_instrument.keys())


def get_instrument_ls(s_name: str) -> list:
    """
    Get instrument list.

    :param s_name: surgery name
    :return: list of instruments
    """
    dc_surgery_instrument = json.load(open(os.path.join(BASE_CORE_DIR, 'data/surgery_to_instruments.json'),
                                           encoding='utf-8'))
    return dc_surgery_instrument[s_name]


def get_consumable_stock(instruments: list) -> list:
    """
    Check if stock has enough consumables for input.

    :param instruments: list of instruments
    :return: list of consumables that do not match
    """
    ls_c_name = get_supply(c_name=get_consumable_ls(instruments=instruments))
    df = pd.DataFrame(ls_c_name)
    df = df[df["description"] == ""].groupby('c_name').count().reset_index().rename(columns={"c_id": "nums"})
    return df[["c_name", "nums"]].to_dict('records')


def _update_and_get_supply(x):
    c_id = get_newest_supply(n_limit=1, c_name=x["c_name"])[0]["c_id"]
    update_supply(c_id=c_id, description=x["description"])
    return get_supply(c_id=c_id)[0]["c_id"]


def insert_surgery_info(ls_c_name: list,
                        ls_i_id: list,
                        p_name: str,
                        admission_number: int,
                        department: str,
                        s_name: str,
                        chief_surgeon: str,
                        associate_surgeon: str,
                        instrument_nurse: Union[list[str], str],
                        circulating_nurse: Union[list[str], str],
                        begin_time: datetime,
                        end_time: datetime):
    """
    Insert a surgery info into database.

    :param ls_i_id: list of instrument id
    :param ls_c_name: list of {c_name: "无菌壁套", description: "默认"}
    :param p_name: patient's name
    :param admission_number: admission number
    :param department: department of chief surgeon
    :param s_name: surgery name
    :param chief_surgeon: chief surgeon
    :param associate_surgeon: associate surgeon
    :param instrument_nurse: instrument nurse
    :param circulating_nurse: circulating nurse
    :param begin_time: surgery's begin time
    :param end_time: surgery's end time
    :return: message of whether successfully inserted
    """
    try:
        instruments = list(map(lambda x: update_instrument_times_info(x)["instrument"]["i_id"], ls_i_id))
        consumables = list(map(lambda x: _update_and_get_supply(x), ls_c_name))
        chief_surgeon = get_user(name=chief_surgeon)["u_id"]
        associate_surgeon = get_user(name=associate_surgeon)["u_id"]
        if isinstance(instrument_nurse, str):
            instrument_nurse = [get_user(name=instrument_nurse)["u_id"]]
        else:
            instrument_nurse = list(map(lambda x: get_user(name=x)["u_id"], instrument_nurse))
        if isinstance(circulating_nurse, str):
            circulating_nurse = [get_user(name=circulating_nurse)["u_id"]]
        else:
            circulating_nurse = list(map(lambda x: get_user(name=x)["u_id"], circulating_nurse))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Input parameters have errors, and raise {e}")
    return insert_surgery(p_name=p_name, admission_number=admission_number, department=department, s_name=s_name,
                          chief_surgeon=chief_surgeon, associate_surgeon=associate_surgeon,
                          instrument_nurse=instrument_nurse, circulating_nurse=circulating_nurse, begin_time=begin_time,
                          end_time=end_time, instruments=instruments, consumables=consumables)
