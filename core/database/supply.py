"""
CURD functions for supplies document
"""
import logging
from datetime import datetime
from typing import Union

from base import supplies

log = logging.getLogger(__name__)


def get_filter(begin_time: datetime = None,
               end_time: datetime = None,
               c_id: Union[int, list[int]] = None,
               c_name: Union[str, list[str]] = None) -> dict:
    """
    Get specific supply filter.

    :param begin_time: insert_time should >= begin_time
    :param end_time: insert_time should < begin_time
    :param c_id: supply id, must be not overlay int
    :param c_name: supply's name
    :return: filter
    """
    f = {}
    if begin_time is not None:
        f["insert_time"] = {"$gte": begin_time}
    if end_time is not None:
        f["insert_time"] = {"$lt": end_time}
    if c_id is not None:
        if isinstance(c_id, int):
            f["c_id"] = c_id
        elif isinstance(c_id, list):
            f["c_id"] = {"$in": c_id}
        else:
            log.error("c_id should be either str or list")
    if c_name is not None:
        if isinstance(c_name, str):
            f["c_name"] = c_name
        elif isinstance(c_name, list):
            f["c_name"] = {"$in": c_name}
        else:
            log.error("c_name should be either str or list")
    return f


def get_supply(begin_time: datetime = None,
               end_time: datetime = None,
               c_id: Union[int, list[int]] = None,
               c_name: Union[str, list[str]] = None):
    """
    Get specific supply.

    :param begin_time: insert_time should >= begin_time
    :param end_time: insert_time should < begin_time
    :param c_id: supply id, must be not overlay int
    :param c_name: supply's name
    :return: filter
    """
    f = get_filter(begin_time=begin_time, end_time=end_time, c_id=c_id, c_name=c_name)
    return list(supplies.find(f, {"_id": 0}))


def insert_supply(c_name: str):
    """
    Insert a specific supply.

    :param c_name: supply's name
    :return: message of whether successfully inserted
    """
    c_id = list(supplies.find().sort([('c_id', -1)]).limit(1))
    if len(c_id) == 0:
        c_id = 0
    else:
        c_id = c_id[0]["c_id"] + 1
    insert_doc = dict(c_id=c_id, c_name=c_name, insert_time=datetime.now())
    try:
        supplies.insert_one(insert_doc)
        return "successful"
    except Exception as e:
        log.error(f"mongodb insert operation in supplies collection failed and raise the following exception: {e}")
        return "unsuccessful"


def delete_instrument(begin_time: datetime = None,
                      end_time: datetime = None,
                      c_id: Union[int, list[int]] = None,
                      c_name: Union[str, list[str]] = None):
    """
    Delete specific supply.

    :param begin_time: insert_time should >= begin_time
    :param end_time: insert_time should < begin_time
    :param c_id: supply id, must be not overlay int
    :param c_name: supply's name
    :return: message of whether successfully deleted
    """
    f = get_filter(c_id=c_id, c_name=c_name, begin_time=begin_time, end_time=end_time)
    try:
        supplies.delete_many(f)
        return "successful"
    except Exception as e:
        log.error(f"mongodb delete operation in apparatus collection failed and raise the following exception: {e}")
        return "unsuccessful"
