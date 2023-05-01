"""
CURD functions for apparatus document
"""
import logging
from typing import Union
from datetime import datetime

from core.database.base import apparatus

log = logging.getLogger(__name__)


def get_filter(begin_time: datetime = None,
               end_time: datetime = None,
               i_id: Union[int, list[int]] = None,
               i_name: Union[str, list[str]] = None,
               times: Union[int, list[int]] = None) -> dict:
    """
    Get specific instrument filter.

    :param begin_time: insert_time should >= begin_time
    :param end_time: insert_time should < begin_time
    :param i_id: instrument id, must be not overlay int
    :param i_name: instrument's name
    :param times: times the instrument used
    :return: filter
    """
    f = {}
    if begin_time is not None:
        f["insert_time"] = {"$gte": begin_time}
    if end_time is not None:
        f["insert_time"] = {"$lt": end_time}
    if i_id is not None:
        if isinstance(i_id, int):
            f["i_id"] = i_id
        elif isinstance(i_id, list):
            f["i_id"] = {"$in": i_id}
        else:
            log.error("i_id should be either str or list")
    if i_name is not None:
        if isinstance(i_name, str):
            f["i_name"] = i_name
        elif isinstance(i_name, list):
            f["i_name"] = {"$in": i_name}
        else:
            log.error("i_name should be either str or list")
    if times is not None:
        if isinstance(times, int):
            f["times"] = times
        elif isinstance(times, list):
            f["times"] = {"$in": times}
        else:
            log.error("times should be either str or list")
    return f


def get_instrument(begin_time: datetime = None,
                   end_time: datetime = None,
                   i_id: Union[int, list[int]] = None,
                   i_name: Union[str, list[str]] = None,
                   times: Union[int, list[int]] = None):
    """
    Get specific instrument.

    :param begin_time: insert_time should >= begin_time
    :param end_time: insert_time should < begin_time
    :param i_id: instrument id, must be not overlay int
    :param i_name: instrument's name
    :param times: times the instrument used
    :return: list of instruments
    """
    f = get_filter(begin_time=begin_time, end_time=end_time, i_id=i_id, i_name=i_name, times=times)
    return list(apparatus.find(f, {"_id": 0}))


def insert_instrument(i_name: str,
                      times: int = 12):
    """
    Insert a specific instrument.

    :param i_name: instrument's name
    :param times: times the instrument used, default is 12
    :return: message of whether successfully inserted
    """
    i_id = list(apparatus.find().sort([('i_id', -1)]).limit(1))
    if len(i_id) == 0:
        i_id = 0
    else:
        i_id = i_id[0]["i_id"] + 1
    insert_doc = dict(i_id=i_id, i_name=i_name, times=times, insert_time=datetime.now())
    try:
        apparatus.insert_one(insert_doc)
        return "successful"
    except Exception as e:
        log.error(f"mongodb insert operation in apparatus collection failed and raise the following exception: {e}")
        return "unsuccessful"


def delete_instrument(begin_time: datetime = None,
                      end_time: datetime = None,
                      i_id: Union[int, list[int]] = None,
                      i_name: Union[str, list[str]] = None,
                      times: Union[int, list[int]] = None):
    """
    Delete specific instrument.

    :param begin_time: insert_time should >= begin_time
    :param end_time: insert_time should < begin_time
    :param i_id: instrument id, must be not overlay int
    :param i_name: instrument's name
    :param times: times the instrument used
    :return: message of whether successfully deleted
    """
    f = get_filter(begin_time=begin_time, end_time=end_time, i_id=i_id, i_name=i_name, times=times)
    try:
        apparatus.delete_many(f)
        return "successful"
    except Exception as e:
        log.error(f"mongodb delete operation in apparatus collection failed and raise the following exception: {e}")
        return "unsuccessful"


def update_instrument(v_times: int,
                      begin_time: datetime = None,
                      end_time: datetime = None,
                      i_id: Union[int, list[int]] = None,
                      i_name: Union[str, list[str]] = None,
                      times: Union[int, list[int]] = None):
    """
    Update specific user. Only support update one user's info.

    :param begin_time: insert_time should >= begin_time
    :param end_time: insert_time should < begin_time
    :param v_times: times need to be updated
    :param i_id: instrument id, must not be overlaid
    :param i_name: instrument's name
    :param times: times the instrument used
    :return: message of whether successfully updated
    """
    if v_times > 12 or v_times < -1:
        log.error("Value error, using times of a certain instrument should be in [-1, 12]")
        return "unsuccessful"
    else:
        new_value = {"$set": {"times": v_times}}
        f = get_filter(begin_time=begin_time, end_time=end_time, i_id=i_id, i_name=i_name, times=times)
        try:
            apparatus.update_many(f, new_value)
            return "successful"
        except Exception as e:
            log.error(f"mongodb delete operation in apparatus collection failed and raise the following exception: {e}")
            return "unsuccessful"
