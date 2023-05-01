"""
CURD functions for user document
"""
import logging
import base64
from typing import Union

from core.database.base import user

log = logging.getLogger(__name__)
user_dict = {"医生": 1, "护士": 2, "管理员": 0}


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
            f["user_type"] = user_dict.get(user_type)
        elif isinstance(user_type, list):
            f["user_type"] = {"$in": list(map(lambda x: user_dict.get(x), user_type))}
        else:
            log.error("user_type should be either int or list")
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
    code = str(base64.b64encode(code.encode('utf-8')))[2:-1]
    insert_doc = dict(u_id=u_id, name=name, user_type=user_dict.get(user_type), code=code)
    try:
        user.insert_one(insert_doc)
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


def update_user(key: str,
                value: any,
                u_id: Union[str, list[str]] = None,
                name: Union[str, list[str]] = None,
                user_type: Union[str, list[str]] = None):
    """
    Update specific user. Only support update one user's info.

    :param key: keys need to be updated
    :param value: values need to be updated
    :param u_id: user's id
    :param name: user's name
    :param user_type: user type
    :return: message of whether successfully updated
    """
    new_value = {"$set": {key: value}}
    f = get_filter(u_id=u_id, name=name, user_type=user_type)
    try:
        user.update_many(f, new_value)
        return "successful"
    except Exception as e:
        log.error(f"mongodb delete operation in user collection failed and raise the following exception: {e}")
        return "unsuccessful"

