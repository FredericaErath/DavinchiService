"""
Administrator end operations
"""
from datetime import datetime
from typing import Union

import pandas as pd
from fastapi import HTTPException

from constant import USER_DICT_REVERSE, USER_COLUMNS, STATUS, PRIORITY
from core.database import get_user, delete_user, insert_users, USER_DICT, get_surgery
from core.database.message import get_message, delete_message, update_message


def get_users(u_id: Union[str, list[str]] = None,
              name: Union[str, list[str]] = None,
              user_type: Union[str, list[str]] = None):
    users = get_user(u_id=u_id, name=name, user_type=user_type)
    if len(users) == 0:
        return []
    else:
        ls_users = list(map(lambda x: {"user_type": USER_DICT_REVERSE.get(x["user_type"]),
                                       "insert_datetime": x["insert_datetime"].strftime("%Y-%m-%d %H:%M:%S"),
                                       "u_id": x["u_id"], "name": x["name"]}, users))
        return ls_users


def delete_user_by_uid(u_id: Union[list, str]):
    res = delete_user(u_id=u_id)
    if res == "unsuccessful":
        raise HTTPException(status_code=400, detail="Something went wrong, please check u_id.")
    else:
        return res


def add_users_by_file(f_users: str):
    df = pd.read_excel(f_users).rename(columns=USER_COLUMNS)
    # check columns
    if set(df.columns.tolist()) == set(USER_COLUMNS.values()):
        df[['u_id', 'code']] = df[['u_id', 'code']].astype('str')
        df["user_type"] = df["user_type"].apply(lambda x: USER_DICT.get(x))
        df["insert_datetime"] = datetime.utcnow()
        return insert_users(df.to_dict('records'))
    else:
        HTTPException(status_code=400, detail="Columns do not fit for restriction.")


def get_message_by_filter(status: str = None,
                          priority: str = None,
                          begin_time: datetime = None,
                          end_time: datetime = None):
    if status:
        status = STATUS.get(status)
    if priority:
        priority = PRIORITY.get(priority)
    res = get_message(status=status, priority=priority, begin_time=begin_time, end_time=end_time)
    if len(res) == 0:
        return []
    else:
        return res


def delete_message_by_mid(m_id: int):
    res = delete_message(m_id=m_id)
    if res == "unsuccessful":
        raise HTTPException(status_code=400, detail="Something went wrong, please check m_id.")
    else:
        return res


def update_message_by_mid(m_id: int, status: str = None, priority: str = None):
    if status:
        status = STATUS.get(status)
    if priority:
        priority = PRIORITY.get(priority)
    res = update_message(m_id=m_id, status=status, priority=priority)
    if res == "unsuccessful":
        raise HTTPException(status_code=400, detail="Something went wrong, please check m_id.")
    else:
        return res

