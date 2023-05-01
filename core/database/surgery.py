"""
CURD functions for surgery document
"""
from datetime import datetime
import logging
from typing import Union

from base import surgery

log = logging.getLogger(__name__)
department_dict = {"肝脾外科": "hepa", "胃肠外科": "gastro",
                   "泌尿外科": "urologic", "胆胰外科": "pancreatic",
                   "胸外科": "chest", "妇科": "gynae", "心脏外科": "cardiac"}


def get_filter(begin_time: datetime = None,
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
            f["department"] = department_dict.get(department)
        elif isinstance(department, list):
            f["department"] = {"$in": list(map(lambda x: department_dict.get(x), department))}
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
        if isinstance(instrument_nurse, str):
            f["instrument_nurse"] = instrument_nurse
        elif isinstance(instrument_nurse, list):
            f["instrument_nurse"] = {"$in": instrument_nurse}
        else:
            log.error("instrument_nurse should be either str or list")
    if circulating_nurse is not None:
        if isinstance(circulating_nurse, str):
            f["circulating_nurse"] = circulating_nurse
        elif isinstance(circulating_nurse, list):
            f["circulating_nurse"] = {"$in": circulating_nurse}
        else:
            log.error("circulating_nurse should be either str or list")
    return f


def get_surgery(begin_time: datetime = None,
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
    f = get_filter(p_name=p_name, admission_number=admission_number, department=department, s_name=s_name,
                   chief_surgeon=chief_surgeon, associate_surgeon=associate_surgeon, instrument_nurse=instrument_nurse,
                   circulating_nurse=circulating_nurse, begin_time=begin_time, end_time=end_time)
    return list(surgery.find(f, {"_id": 0}))


def insert_surgery(p_name: str,
                   admission_number: int,
                   department: str,
                   s_name: str,
                   chief_surgeon: str,
                   associate_surgeon: str,
                   instrument_nurse: str,
                   circulating_nurse: str,
                   begin_time: datetime,
                   end_time: datetime,
                   instruments: list[dict],
                   consumables: list[dict]):
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
    :param instruments: instruments
    :param consumables: consumables
    :return: message of whether successfully inserted
    """
    try:
        insert_doc = dict(p_name=p_name, date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                          admission_number=admission_number, department=department_dict.get(department), s_name=s_name,
                          chief_surgeon=chief_surgeon, associate_surgeon=associate_surgeon,
                          instrument_nurse=instrument_nurse, circulating_nurse=circulating_nurse, begin_time=begin_time,
                          end_time=end_time, instruments=instruments, consumables=consumables)
        surgery.insert_one(insert_doc)
        return "successful"
    except Exception as e:
        log.error(f"mongodb insert operation in surgery collection failed and raise the following exception: {e}")
        return "unsuccessful"


def delete_surgery(begin_time: datetime = None,
                   end_time: datetime = None,
                   department: Union[str, list[str]] = None,
                   s_name: Union[str, list[str]] = None,
                   chief_surgeon: Union[str, list[str]] = None,
                   associate_surgeon: Union[str, list[str]] = None,
                   instrument_nurse: Union[str, list[str]] = None,
                   circulating_nurse: Union[str, list[str]] = None):
    """
        Delete one doc in surgery document.

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
    f = get_filter(department=department, s_name=s_name, chief_surgeon=chief_surgeon,
                   associate_surgeon=associate_surgeon, instrument_nurse=instrument_nurse,
                   circulating_nurse=circulating_nurse, begin_time=begin_time, end_time=end_time)
    try:
        surgery.delete_many(f)
        return "successful"
    except Exception as e:
        log.error(f"mongodb delete operation in surgery collection failed and raise the following exception: {e}")
        return "unsuccessful"
