"""
Nurse end operations
"""
from datetime import datetime

from core.database import get_instrument, update_instrument, insert_surgery, update_supply, get_supply, \
    get_newest_supply


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
            return {"msg": "successfully updated instrument times info", "times": times}
        else:
            return {"msg": "something went wrong when updating instrument info", "times": times}
    else:
        return {"msg": "The instrument is dumped", "times": times}


def insert_surgery_info(ls_i_id: list,
                        ls_c_name: list,
                        p_name: str,
                        admission_number: int,
                        department: str,
                        s_name: str,
                        chief_surgeon: str,
                        associate_surgeon: str,
                        instrument_nurse: str,
                        circulating_nurse: str,
                        begin_time: datetime,
                        end_time: datetime):
    """
    Insert a surgery info into database.

    :param ls_i_id: list of instrument id
    :param ls_c_id: list of consumables name
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
    instruments = get_instrument(i_id=ls_i_id)
    # TODO: there's a map between instruments and supplies, once get instruments, we can get maps. We get the latest
    #  supplies' ids without descriptions and update their descriptions
    supplies = list(map(lambda x: get_newest_supply(n_limit=x.n, c_name=x.c_name), ))

