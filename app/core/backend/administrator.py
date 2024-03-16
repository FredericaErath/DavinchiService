"""
Administrator end operations
"""
from datetime import datetime
from typing import Union

import pandas as pd
from fastapi import HTTPException

from app.constant import USER_DICT_REVERSE, USER_COLUMNS, STATUS, PRIORITY, STATUS_R, PRIORITY_R
from app.core.database import get_user, delete_user, insert_users, USER_DICT
from app.core.database.message import get_message, delete_message, update_message
from app.core.backend.auth import AuthHandler

auth = AuthHandler()


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
        df['code'] = df['code'].apply(lambda x: auth.get_pwd_hash(pwd=x))
        df["user_type"] = df["user_type"].apply(lambda x: USER_DICT.get(x))
        df["insert_datetime"] = datetime.utcnow()
        return insert_users(df.to_dict('records'))
    else:
        HTTPException(status_code=400, detail="Columns do not fit for restriction.")


def get_message_by_filter(status: Union[list[str], str] = None,
                          priority: Union[list[str], str] = None,
                          begin_time: datetime = None,
                          end_time: datetime = None,
                          u_id: str = None):
    if status:
        if isinstance(status, str):
            status = STATUS.get(status)
        elif isinstance(status, list):
            status = list(map(lambda x: STATUS.get(x), status))
        else:
            raise HTTPException(status_code=400, detail="Something went wrong, please check status.")
    if priority:
        if isinstance(priority, str):
            priority = PRIORITY.get(priority)
        elif isinstance(priority, list):
            priority = list(map(lambda x: PRIORITY.get(x), priority))
        else:
            raise HTTPException(status_code=400, detail="Something went wrong, please check priority.")
    res = get_message(status=status, priority=priority, begin_time=begin_time, end_time=end_time, u_id=u_id)
    if len(res) == 0:
        return []
    else:
        def _format_message(x):
            x["status"] = STATUS_R.get(x["status"])
            x["priority"] = PRIORITY_R.get(x["priority"])
            x["insert_time"] = x["insert_time"].strftime("%Y-%m-%d %H:%M:%S")
            return x

        res = list(map(lambda x: _format_message(x), res))
        return res


def delete_message_by_mid(m_id: int):
    res = delete_message(m_id=m_id)
    if res == "unsuccessful":
        raise HTTPException(status_code=400, detail="Something went wrong, please check m_id.")
    else:
        return res


def update_message_by_mid(m_id: int, status: str = None, priority: str = None, feedback: str = None):
    if status:
        status = STATUS.get(status)
    if priority:
        priority = PRIORITY.get(priority)
    res = update_message(m_id=m_id, status=status, priority=priority, feedback=feedback)
    if res == "unsuccessful":
        raise HTTPException(status_code=400, detail="Something went wrong, please check m_id.")
    else:
        return res
