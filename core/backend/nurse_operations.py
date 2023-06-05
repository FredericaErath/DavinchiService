"""
Nurse end operations
"""
import logging
from datetime import datetime
import json
import pandas as pd
from core.database import get_instrument, update_instrument, insert_surgery, update_supply, get_supply, \
    get_newest_supply

log = logging.getLogger(__name__)
DC_INSTRUMENT_TO_SUPPLY = {"电剪": "尖端盖附件"}
DC_SUPPLY_TO_NUMBER = {"无菌壁套": 4, "中心柱无菌套": 1, "尖端盖附件": 1}


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
    if "电剪" in list(map(lambda x: x["i_name"], instruments)):
        ls_consumables += ["尖端盖附件"]
    return ls_consumables


def get_surgery_name():
    """
    Get surgery list.

    :return: list of surgeries
    """
    dc_surgery_instrument = json.load(open('../data/surgery_to_instruments.json', encoding='utf-8'))
    return list(dc_surgery_instrument.keys())


def get_instrument_ls(s_name: str) -> list:
    """
    Get instrument list.

    :param s_name: surgery name
    :return: list of instruments
    """
    dc_surgery_instrument = json.load(open('../data/surgery_to_instruments.json', encoding='utf-8'))
    return dc_surgery_instrument[s_name]


def check_consumable_stock(ls_c_name: list) -> list:
    """
    Check if stock has enough consumables for input.

    :param ls_c_name: list of {c_name: "无菌壁套", description: "默认"}
    :return: list of consumables that do not match
    """
    df = pd.DataFrame(ls_c_name).groupby("c_name").count().reset_index()
    df["num"] = df.apply(lambda x: len(get_newest_supply(c_name=x["c_name"], n_limit=x["description"])), axis=1)
    return df[df["num"] != df["description"]]["c_name"].to_list()


def _update_and_get_supply(x, ls_c_id):
    c_id = get_newest_supply(n_limit=1, c_name=x["c_name"])[0]["c_id"]
    ls_c_id += [c_id]
    update_supply(c_id=c_id, description=x["description"])
    return get_supply(c_id=c_id)[0]


def insert_surgery_info(ls_c_name: list,
                        ls_i_id: list,
                        p_name: str,
                        admission_number: int,
                        department: str,
                        s_name: str,
                        chief_surgeon: str,
                        associate_surgeon: str,
                        instrument_nurse: str,
                        circulating_nurse: str,
                        begin_time: datetime,
                        end_time: datetime,
                        part: str = None):
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
    :param part: part of the surgery operate on
    :return: message of whether successfully inserted
    """
    ls_c_id = []
    instruments = list(map(lambda x: update_instrument_times_info(x)["instrument"], ls_i_id))
    consumables = list(map(lambda x: _update_and_get_supply(x, ls_c_id), ls_c_name))
    return insert_surgery(p_name=p_name, admission_number=admission_number, department=department, s_name=s_name,
                          chief_surgeon=chief_surgeon, associate_surgeon=associate_surgeon,
                          instrument_nurse=instrument_nurse, circulating_nurse=circulating_nurse, begin_time=begin_time,
                          end_time=end_time, instruments=instruments, consumables=consumables, part=part)
