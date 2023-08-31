"""
CURD functions for supplies document
"""
import logging
from datetime import datetime
from typing import Union

from core.database.base import supplies

log = logging.getLogger(__name__)


def get_filter(begin_time: datetime = None,
               end_time: datetime = None,
               c_id: Union[int, list[int]] = None,
               c_name: Union[str, list[str]] = None,
               description: Union[str, list[str]] = None,
               validity: bool = None) -> dict:
    """
    Get supply filter.

    :param begin_time: insert_time should >= begin_time
    :param end_time: insert_time should < begin_time
    :param c_id: supply id, must be not overlay int
    :param c_name: supply's name
    :param description: supply's description
    :param validity: true or false
    :return: filter
    """
    f = {}
    if begin_time is not None and end_time is None:
        f["insert_time"] = {"$gte": begin_time}
    if end_time is not None and begin_time is None:
        f["insert_time"] = {"$lt": end_time}
    if begin_time is not None and end_time is not None:
        f["insert_time"] = {"$lt": end_time, "$gte": begin_time}
    if c_id is not None:
        if isinstance(c_id, int):
            f["c_id"] = c_id
        elif isinstance(c_id, list):
            f["c_id"] = {"$in": c_id}
        else:
            log.error("c_id should be either int or list")
    if c_name is not None:
        if isinstance(c_name, str):
            f["c_name"] = c_name
        elif isinstance(c_name, list):
            f["c_name"] = {"$in": c_name}
        else:
            log.error("c_name should be either str or list")
    if description is not None:
        if isinstance(description, str):
            f["description"] = description
        elif isinstance(description, list):
            f["description"] = {"$in": description}
        else:
            log.error("description should be either str or list")
    if validity is not None:
        if validity is True:
            f["description"] = ""
        else:
            f["description"] = {"$ne": ""}
    return f


def get_supply(begin_time: datetime = None,
               end_time: datetime = None,
               c_id: Union[int, list[int]] = None,
               c_name: Union[str, list[str]] = None,
               description: Union[str, list[str]] = None,
               validity: bool = None):
    """
    Get specific supply.

    :param begin_time: insert_time should >= begin_time
    :param end_time: insert_time should < begin_time
    :param c_id: supply id, must be not overlay int
    :param c_name: supply's name
    :param description: supply's description
    :param validity: true or false
    :return: filter
    """
    f = get_filter(begin_time=begin_time, end_time=end_time, c_id=c_id, c_name=c_name, description=description,
                   validity=validity)
    return list(supplies.find(f, {"_id": 0}))


def get_newest_supply(n_limit: int, c_name: str):
    res = list(supplies.find({"description": "", "c_name": c_name}, {"_id": 0}).sort([('c_id', -1)]).limit(n_limit))
    return res


def insert_supply(c_name: str,
                  description: str = ""):
    """
    Insert a specific supply.

    :param c_name: supply's name
    :param description: supply's description
    :return: message of whether successfully inserted
    """
    c_id = list(supplies.find().sort([('c_id', -1)]).limit(1))
    if len(c_id) == 0:
        c_id = 0
    else:
        c_id = c_id[0]["c_id"] + 1
    insert_doc = dict(c_id=c_id, c_name=c_name, insert_time=datetime.now(), description=description)
    try:
        supplies.insert_one(insert_doc)
        return "successful"
    except Exception as e:
        log.error(f"mongodb insert operation in supplies collection failed and raise the following exception: {e}")
        return "unsuccessful"


def delete_supply(begin_time: datetime = None,
                  end_time: datetime = None,
                  c_id: Union[int, list[int]] = None,
                  c_name: Union[str, list[str]] = None,
                  description: Union[str, list[str]] = None):
    """
    Delete specific supply.

    :param begin_time: insert_time should >= begin_time
    :param end_time: insert_time should < begin_time
    :param c_id: supply id, must be not overlay int
    :param c_name: supply's name
    :param description: supply's description
    :return: message of whether successfully deleted
    """
    f = get_filter(c_id=c_id, c_name=c_name, begin_time=begin_time, end_time=end_time, description=description)
    try:
        supplies.delete_many(f)
        return "successful"
    except Exception as e:
        log.error(f"mongodb delete operation in apparatus collection failed and raise the following exception: {e}")
        return "unsuccessful"


def update_supply(begin_time: datetime = None,
                  end_time: datetime = None,
                  c_id: Union[int, list[int]] = None,
                  c_name: Union[str, list[str]] = None,
                  description: Union[str, list[str]] = None):
    """
    Delete specific supply.

    :param begin_time: insert_time should >= begin_time
    :param end_time: insert_time should < begin_time
    :param c_id: supply id, must be not overlay int
    :param c_name: supply's name
    :param description: supply's description
    :return: message of whether successfully updated
    """
    new_value = {"$set": {"description": description}}
    f = get_filter(begin_time=begin_time, end_time=end_time, c_id=c_id, c_name=c_name)
    try:
        supplies.update_many(f, new_value)
        return "successful"
    except Exception as e:
        log.error(f"mongodb delete operation in supplies collection failed and raise the following exception: {e}")
        return "unsuccessful"

