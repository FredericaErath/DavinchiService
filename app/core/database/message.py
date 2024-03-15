"""
CURD functions for message document
"""
import logging
from datetime import datetime
from typing import Union

from app.core.database.base import message

log = logging.getLogger(__name__)


def get_filter(m_id: Union[int, list] = None,
               status: Union[list[int], int] = None,
               priority: Union[list[int], int] = None,
               u_id: str = None,
               u_name: str = None,
               time: datetime = None,
               begin_time: datetime = None,
               end_time: datetime = None):
    """
    Get message filter.

    :param m_id: message id
    :param status: status of the message, {0: unreviewed, 1: pending, 2: done}
    :param priority: priority of the message, {0: unimportant, 1: normal, 2: important}
    :param u_id: user's id who send the message.
    :param u_name: user's name who send the message.
    :param time: sending time
    :param begin_time: begin time
    :param end_time: end time
    :return: filter
    """
    f = {}
    if m_id is not None:
        if isinstance(m_id, int):
            f["m_id"] = m_id
        elif isinstance(m_id, list):
            f["m_id"] = {"$in": m_id}
        else:
            log.error("m_id should be either str or list")
    if status:
        if isinstance(status, int):
            f["status"] = status
        elif isinstance(status, list):
            f["status"] = {"$in": status}
        else:
            log.error("status should be either str or list")
    if priority:
        if isinstance(priority, int):
            f["priority"] = priority
        elif isinstance(priority, list):
            f["priority"] = {"$in": priority}
        else:
            log.error("priority should be either str or list")
    if begin_time and not end_time:
        f["insert_time"] = {"$gte": begin_time}
    if end_time and not begin_time:
        f["insert_time"] = {"$lt": end_time}
    if begin_time and not end_time:
        f["insert_time"] = {"$lt": end_time, "$gte": begin_time}
    if u_id is not None:
        f["u_id"] = u_id
    if u_name:
        f["u_name"] = u_name
    if time:
        f["insert_time"] = time
    return f


def get_message(m_id: int = None,
                status: Union[list[int], int] = None,
                priority: Union[list[int], int] = None,
                u_id: str = None,
                u_name: str = None,
                time: datetime = None,
                begin_time: datetime = None,
                end_time: datetime = None):
    """
    Get message.

    :param m_id: message id
    :param status: status of the message, {0: unreviewed, 1: pending, 2: done}
    :param priority: priority of the message, {0: unimportant, 1: normal, 2: important}
    :param u_id: user's id who send the message.
    :param u_name: user's name who send the message.
    :param time: sending time
    :param begin_time: begin time
    :param end_time: end time
    :return: message
    """
    f = get_filter(m_id=m_id, status=status, priority=priority,
                   u_id=u_id, u_name=u_name, time=time, begin_time=begin_time, end_time=end_time)
    return list(message.find(f, {"_id": 0}))


def insert_message(u_id: str, u_name: str, content: str):
    """
    Insert message.
    """
    last_m_id = list(message.find().sort([('m_id', -1)]).limit(1))
    # get last message id
    if len(last_m_id) == 0:
        m_id = 0
    else:
        m_id = last_m_id[0]["m_id"] + 1

    insert_doc = dict(m_id=m_id, status=1, priority=1, feedback="NULL",
                      u_id=u_id, u_name=u_name, insert_time=datetime.utcnow(), content=content)
    try:
        message.insert_one(insert_doc)
        return "successful"
    except Exception as e:
        log.error(f"mongodb insert operation in user collection failed and raise the following exception: {e}")
        return "unsuccessful"


def delete_message(m_id: Union[int, list] = None,
                   status: Union[list[int], int] = None,
                   priority: Union[list[int], int] = None,
                   u_id: str = None,
                   u_name: str = None,
                   time: datetime = None,
                   begin_time: datetime = None,
                   end_time: datetime = None):
    """
    Delete message.

    :param m_id: message id
    :param status: status of the message, {0: unreviewed, 1: pending, 2: done}
    :param priority: priority of the message, {0: unimportant, 1: normal, 2: important}
    :param u_id: user's id who send the message.
    :param u_name: user's name who send the message.
    :param time: sending time
    :param begin_time: begin time
    :param end_time: end time
    :return: delete operation message.
    """
    f = get_filter(m_id=m_id, status=status, priority=priority,
                   u_id=u_id, u_name=u_name, time=time, begin_time=begin_time, end_time=end_time)
    try:
        message.delete_many(f)
        return "successful"
    except Exception as e:
        log.error(f"mongodb delete operation in user collection failed and raise the following exception: {e}")
        return "unsuccessful"


def update_message(m_id: int, status: int = None, priority: int = None, feedback: str = None):
    """
    Update message.

    :param m_id: message id
    :param status: status of the message, {0: unreviewed, 1: pending, 2: done}
    :param priority: priority of the message, {0: unimportant, 1: normal, 2: important}
    :param feedback: feedback from administrator
    :return: update message
    """
    f = get_filter(m_id=m_id)
    new_value = {}
    if status:
        new_value["status"] = status
    if priority:
        new_value["priority"] = priority
    if feedback:
        new_value["feedback"] = feedback
    try:
        message.update_many(f, {"$set": new_value})
        return "successful"
    except Exception as e:
        log.error(f"mongodb update operation in apparatus collection failed and raise the following exception: {e}")
        return "unsuccessful"
