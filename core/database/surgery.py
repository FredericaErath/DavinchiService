"""
CURD functions for surgery document
"""
from datetime import datetime
import logging
from typing import Union

from constant import DC_DEPARTMENT, LS_PART
from core.database.base import surgery

log = logging.getLogger(__name__)


def get_filter(s_id: int = None,
               begin_time: datetime = None,
               end_time: datetime = None,
               p_name: Union[str, list[str]] = None,
               admission_number: Union[int, list[int]] = None,
               department: Union[str, list[str]] = None,
               s_name: Union[str, list[str]] = None,
               chief_surgeon: Union[str, list[str]] = None,
               associate_surgeon: Union[str, list[str]] = None,
               instrument_nurse: Union[str, list[str]] = None,
               circulating_nurse: Union[str, list[str]] = None):
    """
    Get specific surgery filter.

    :param s_id: surgery id
    :param begin_time: begin time
    :param end_time: end time
    :param p_name: patient's name
    :param admission_number: admission number
    :param department: department of chief surgeon
    :param s_name: surgery name
    :param chief_surgeon: chief surgeon
    :param associate_surgeon: associate surgeon
    :param instrument_nurse: instrument nurse
    :param circulating_nurse: circulating nurse
    :return: filter
    """
    f = {}
    if s_id is not None:
        f["s_id"] = s_id
    if begin_time is not None:
        f["date"] = {"$gte": begin_time}
    if end_time is not None:
        f["date"] = {"$lt": end_time}
    if p_name is not None:
        if isinstance(p_name, int):
            f["p_name"] = p_name
        elif isinstance(p_name, list):
            f["p_name"] = {"$in": p_name}
        else:
            log.error("p_name should be either str or list")
    if admission_number is not None:
        if isinstance(admission_number, int):
            f["admission_number"] = admission_number
        elif isinstance(admission_number, list):
            f["admission_number"] = {"$in": admission_number}
        else:
            log.error("admission_number should be either int or list")
    if department is not None:
        if isinstance(department, str):
            f["department"] = DC_DEPARTMENT.get(department)
        elif isinstance(department, list):
            f["department"] = {"$in": list(map(lambda x: DC_DEPARTMENT.get(x), department))}
        else:
            log.error("department should be either str or list")
    if s_name is not None:
        if isinstance(s_name, str):
            f["s_name"] = s_name
        elif isinstance(s_name, list):
            f["s_name"] = {"$in": s_name}
        else:
            log.error("s_name should be either str or list")
    if chief_surgeon is not None:
        if isinstance(chief_surgeon, str):
            f["chief_surgeon"] = chief_surgeon
        elif isinstance(chief_surgeon, list):
            f["chief_surgeon"] = {"$in": chief_surgeon}
        else:
            log.error("chief_surgeon should be either str or list")
    if associate_surgeon is not None:
        if isinstance(associate_surgeon, str):
            f["associate_surgeon"] = associate_surgeon
        elif isinstance(associate_surgeon, list):
            f["associate_surgeon"] = {"$in": associate_surgeon}
        else:
            log.error("associate_surgeon should be either str or list")
    if instrument_nurse is not None:
        # TODO: xxx参加过的手术？
        f["instrument_nurse"] = {"$in": instrument_nurse}
    if circulating_nurse is not None:
        f["circulating_nurse"] = {"$in": circulating_nurse}
    return f


def get_surgery(s_id: int = None,
                begin_time: datetime = None,
                end_time: datetime = None,
                p_name: Union[str, list[str]] = None,
                admission_number: Union[int, list[int]] = None,
                department: Union[str, list[str]] = None,
                s_name: Union[str, list[str]] = None,
                chief_surgeon: Union[str, list[str]] = None,
                associate_surgeon: Union[str, list[str]] = None,
                instrument_nurse: Union[str, list[str]] = None,
                circulating_nurse: Union[str, list[str]] = None):
    """
    Get specific surgery filter.

    :param s_id: surgery id
    :param begin_time: begin time
    :param end_time: end time
    :param p_name: patient's name
    :param admission_number: admission number
    :param department: department of chief surgeon
    :param s_name: surgery name
    :param chief_surgeon: chief surgeon
    :param associate_surgeon: associate surgeon
    :param instrument_nurse: instrument nurse
    :param circulating_nurse: circulating nurse
    :return: message of whether successfully inserted
    """
    f = get_filter(s_id=s_id, p_name=p_name, admission_number=admission_number, department=department,
                   s_name=s_name,
                   chief_surgeon=chief_surgeon, associate_surgeon=associate_surgeon, instrument_nurse=instrument_nurse,
                   circulating_nurse=circulating_nurse, begin_time=begin_time, end_time=end_time)
    return list(surgery.find(f, {"_id": 0}))


def insert_surgery(p_name: str,
                   admission_number: int,
                   department: str,
                   s_name: str,
                   chief_surgeon: str,
                   associate_surgeon: str,
                   instrument_nurse: list[str],
                   circulating_nurse: list[str],
                   begin_time: datetime,
                   end_time: datetime,
                   instruments: list[int],
                   consumables: list[int]):
    """
    Add one doc in surgery document.

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
    :param instruments: instruments, format in {id: 1, description: "默认"}
    :param consumables: consumables, format in {id: 1, description: "默认"}
    :return: message of whether successfully inserted
    """
    s_id = list(surgery.find().sort([('s_id', -1)]).limit(1))
    if len(s_id) == 0:
        s_id = 0
    else:
        s_id = s_id[0]["s_id"] + 1

    try:
        if s_name not in LS_PART:
            part = ""
        insert_doc = dict(s_id=s_id, p_name=p_name,
                          date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                          admission_number=admission_number, department=DC_DEPARTMENT.get(department), s_name=s_name,
                          chief_surgeon=chief_surgeon, associate_surgeon=associate_surgeon,
                          instrument_nurse=instrument_nurse, circulating_nurse=circulating_nurse, begin_time=begin_time,
                          end_time=end_time, instruments=instruments, consumables=consumables)
        surgery.insert_one(insert_doc)
        return "successful"
    except Exception as e:
        log.error(f"mongodb insert operation in surgery collection failed and raise the following exception: {e}")
        return "unsuccessful"


def delete_surgery(s_id: int = None,
                   begin_time: datetime = None,
                   end_time: datetime = None,
                   department: Union[str, list[str]] = None,
                   s_name: Union[str, list[str]] = None,
                   chief_surgeon: Union[str, list[str]] = None,
                   associate_surgeon: Union[str, list[str]] = None,
                   instrument_nurse: Union[str, list[str]] = None,
                   circulating_nurse: Union[str, list[str]] = None):
    """
        Delete one doc in surgery document.

        :param s_id: surgery id
        :param department: department of chief surgeon
        :param s_name: surgery name
        :param chief_surgeon: chief surgeon
        :param associate_surgeon: associate surgeon
        :param instrument_nurse: instrument nurse
        :param circulating_nurse: circulating nurse
        :param begin_time: surgery's begin time
        :param end_time: surgery's end time
        :return: message of whether successfully deleted
        """
    f = get_filter(s_id=s_id, department=department, s_name=s_name, chief_surgeon=chief_surgeon,
                   associate_surgeon=associate_surgeon, instrument_nurse=instrument_nurse,
                   circulating_nurse=circulating_nurse, begin_time=begin_time, end_time=end_time)
    try:
        surgery.delete_many(f)
        return "successful"
    except Exception as e:
        log.error(f"mongodb delete operation in surgery collection failed and raise the following exception: {e}")
        return "unsuccessful"


def update_surgery(s_id: int,
                   begin_time: datetime = None,
                   end_time: datetime = None,
                   date: datetime = None,
                   admission_number: int = None,
                   department: str = None,
                   s_name: str = None,
                   chief_surgeon: str = None,
                   associate_surgeon: str = None,
                   instrument_nurse: list = None,
                   circulating_nurse: list = None,
                   instruments: list = None,
                   consumables: list = None):
    """
    Update one surgery info based on surgery id.

    :param admission_number: admission number
    :param date: date of the surgery
    :param s_id: surgery id
    :param department: department of chief surgeon
    :param s_name: surgery name
    :param chief_surgeon: chief surgeon
    :param associate_surgeon: associate surgeon
    :param instrument_nurse: instrument nurse
    :param circulating_nurse: circulating nurse
    :param begin_time: surgery's begin time
    :param end_time: surgery's end time
    :param instruments: instruments info
    :param consumables: consumables info
    :return: update message
    """
    dc_set = {}
    if begin_time is not None:
        dc_set["begin_time"] = begin_time
    if date is not None:
        dc_set["date"] = date
    if admission_number is not None:
        dc_set["admission_number"] = admission_number
    if end_time is not None:
        dc_set["end_time"] = end_time
    if department is not None:
        dc_set["department"] = DC_DEPARTMENT.get(department)
    if s_name is not None:
        dc_set["s_name"] = s_name
    if associate_surgeon is not None:
        dc_set["associate_surgeon"] = associate_surgeon
    if chief_surgeon is not None:
        dc_set["chief_surgeon"] = chief_surgeon
    if instrument_nurse is not None:
        dc_set["instrument_nurse"] = instrument_nurse
    if circulating_nurse is not None:
        dc_set["circulating_nurse"] = circulating_nurse
    if consumables is not None:
        dc_set["consumables"] = consumables
    if instruments is not None:
        dc_set["instruments"] = instruments
    new_value = {"$set": dc_set}
    f = get_filter(s_id=s_id)
    try:
        surgery.update_many(f, new_value)
        return "successful"
    except Exception as e:
        log.error(f"mongodb update operation in user collection failed and raise the following exception: {e}")
        return "unsuccessful"
