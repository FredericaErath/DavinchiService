from datetime import datetime
from typing import Union

from fastapi import HTTPException

from core.database import get_supply, update_supply, insert_supply, delete_supply


def get_supply_general(begin_time: datetime = None,
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
    supplies = get_supply(begin_time=begin_time, end_time=end_time, c_id=c_id, c_name=c_name, description=description,
                          validity=validity)
    if len(supplies) == 0:
        return []
    else:
        return supplies


def update_supply_description(c_id: int, description: str):
    res = update_supply(c_id=c_id, description=description)
    if res == "unsuccessful":
        raise HTTPException(status_code=400, detail="Update failed. Please check the input info.")
    else:
        return res


def insert_supplies(c_name: str, num: int):
    """
    Insert supplies based on num
    """
    for i in range(num):
        res = insert_supply(c_name=c_name)
        if res == "unsuccessful":
            raise HTTPException(status_code=400, detail="Insert failed. Please check the input info.")
    return "successful"


def delete_supply_by_id(c_id: Union[int, list[int]]):
    """
    Delete supplies by id
    """
    res = delete_supply(c_id=c_id)
    if res == "unsuccessful":
        raise HTTPException(status_code=400, detail="Delete failed. Please check the input info.")
    else:
        return res

