"""
CURD functions for user document
"""
import logging
from typing import Union
from datetime import datetime

from constant import USER_DICT
from app.core.database.base import user

log = logging.getLogger(__name__)


def get_filter(u_id: Union[str, list[str]] = None,
               name: Union[str, list[str]] = None,
               user_type: Union[str, list[str]] = None) -> dict:
    """
    Get specific user filter.

    :param u_id: user's id
    :param name: user's name
    :param user_type: user type
    :return: filter
    """
    f = {}
    if u_id is not None:
        if isinstance(u_id, str):
            f["u_id"] = u_id
        elif isinstance(u_id, list):
            f["u_id"] = {"$in": u_id}
        else:
            log.error("u_id should be either str or list")
    if name is not None:
        if isinstance(name, str):
            f["name"] = name
        elif isinstance(name, list):
            f["name"] = {"$in": name}
        else:
            log.error("name should be either str or list")
    if user_type is not None:
        if isinstance(user_type, str):
            f["user_type"] = USER_DICT.get(user_type)
        elif isinstance(user_type, list):
            f["user_type"] = {"$in": list(map(lambda x: USER_DICT.get(x), user_type))}
        else:
            log.error("user_type should be either str or list")
    return f


def get_user(u_id: Union[str, list[str]] = None,
             name: Union[str, list[str]] = None,
             user_type: Union[str, list[str]] = None):
    """
    Get specific user.

    :param u_id: user's id
    :param name: user's name
    :param user_type: user type
    :return: specific user's info
    """
    f = get_filter(u_id=u_id, name=name, user_type=user_type)
    return list(user.find(f, {"_id": 0}))


def insert_user(u_id: str, name: str, user_type: str, code: str):
    """
    Insert a specific user, user's code should be encrypted.

    :param u_id: user's id
    :param name: user's name
    :param user_type: user type
    :param code: user's code
    :return: message of whether successfully inserted
    """
    insert_doc = dict(u_id=u_id, name=name, user_type=USER_DICT.get(user_type), code=code,
                      insert_datetime=datetime.utcnow())
    try:
        user.insert_one(insert_doc)
        return "successful"
    except Exception as e:
        log.error(f"mongodb insert operation in user collection failed and raise the following exception: {e}")
        return "unsuccessful"


def insert_users(users: list):
    """
    Insert a specific user, user's code should be encrypted.

    :param users: dict of users, should be {"u_id": "18851438132", "name": "子淇", "user_type": 0, "code": "16s54vhd"}
    :return: message of whether successfully inserted
    """
    try:
        user.insert_many(users)
        return "successful"
    except Exception as e:
        log.error(f"mongodb insert operation in user collection failed and raise the following exception: {e}")
        return "unsuccessful"


def delete_user(u_id: Union[str, list[str]] = None,
                name: Union[str, list[str]] = None,
                user_type: Union[str, list[str]] = None):
    """
    Delete specific user.

    :param u_id: user's id
    :param name: user's name
    :param user_type: user type
    :return: message of whether successfully deleted
    """
    f = get_filter(u_id=u_id, name=name, user_type=user_type)
    try:
        user.delete_many(f)
        return "successful"
    except Exception as e:
        log.error(f"mongodb delete operation in user collection failed and raise the following exception: {e}")
        return "unsuccessful"


def update_user(u_id: Union[str, list[str]] = None,
                name: str = None,
                user_type: str = None,
                pwd: str = None,
                new_id: str = None):
    """
    Update specific user. Only support update one user's info.

    :param u_id: user's id
    :param name: user's name
    :param user_type: user type
    :param pwd: user's password
    :param new_id: new user's id, in case for changing phone number
    :return: message of whether successfully updated
    """
    dc_set = {}
    if name is not None:
        dc_set["name"] = name
    if user_type is not None:
        dc_set["user_type"] = USER_DICT.get(user_type)
    if pwd is not None:
        dc_set["code"] = pwd
    if new_id is not None:
        if isinstance(u_id, list):
            log.error(f"User's id should be unique")
            return "unsuccessful"
        else:
            dc_set["u_id"] = new_id
    new_value = {"$set": dc_set}
    f = get_filter(u_id=u_id)
    try:
        user.update_many(f, new_value)
        return "successful"
    except Exception as e:
        log.error(f"mongodb delete operation in user collection failed and raise the following exception: {e}")
        return "unsuccessful"
