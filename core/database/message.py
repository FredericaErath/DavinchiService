"""
CURD functions for message document
"""
import logging
from datetime import datetime

from core.database.base import message

log = logging.getLogger(__name__)


def get_filter(u_id: str = None,
               u_name: str = None,
               time: datetime = None,
               begin_time: datetime = None,
               end_time: datetime = None):
    """
    Get message filter.

    :param u_id: user's id who send the message.
    :param u_name: user's name who send the message.
    :param time: sending time
    :param begin_time: begin time
    :param end_time: end time
    :return: filter
    """
    f = {}
    if begin_time and not end_time:
        f["insert_time"] = {"$gte": begin_time}
    if end_time and not begin_time:
        f["insert_time"] = {"$lt": end_time}
    if begin_time and not end_time:
        f["insert_time"] = {"$lt": end_time, "$gte": begin_time}
    if u_id:
        f["u_id"] = u_id
    if u_name:
        f["u_name"] = u_name
    if time:
        f["insert_time"] = time
    return f


def get_message(u_id: str = None,
                u_name: str = None,
                time: datetime = None,
                begin_time: datetime = None,
                end_time: datetime = None):
    """
    Get message.

    :param u_id: user's id who send the message.
    :param u_name: user's name who send the message.
    :param time: sending time
    :param begin_time: begin time
    :param end_time: end time
    :return: message
    """
    f = get_filter(u_id=u_id, u_name=u_name, time=time, begin_time=begin_time, end_time=end_time)
    return list(message.find(f, {"_id": 0}))


def insert_message(u_id: str, u_name: str, content: str):
    """
    Insert message.
    """
    insert_doc = dict(u_id=u_id, u_name=u_name, insert_time=datetime.utcnow(), content=content)
    try:
        message.insert_one(insert_doc)
        return "successful"
    except Exception as e:
        log.error(f"mongodb insert operation in user collection failed and raise the following exception: {e}")
        return "unsuccessful"


def delete_message(u_id: str = None,
                   u_name: str = None,
                   time: datetime = None,
                   begin_time: datetime = None,
                   end_time: datetime = None):
    """
    Delete message.

    :param u_id: user's id who send the message.
    :param u_name: user's name who send the message.
    :param time: sending time
    :param begin_time: begin time
    :param end_time: end time
    :return: delete operation message.
    """
    f = get_filter(u_id=u_id, u_name=u_name, time=time, begin_time=begin_time, end_time=end_time)
    try:
        message.delete_many(f)
        return "successful"
    except Exception as e:
        log.error(f"mongodb delete operation in user collection failed and raise the following exception: {e}")
        return "unsuccessful"
