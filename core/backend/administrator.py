"""
Administrator end operations
"""
from datetime import datetime
from typing import Union

import pandas as pd
from fastapi import HTTPException, UploadFile

from core.database import get_user, delete_user, insert_users, USER_DICT

USER_DICT_REVERSE = {1: "医生", 2: "护士", 0: "管理员"}
COLUMNS = {"账号": "u_id", "用户名称": "name", "用户类型": "user_type", "密码": "code"}


def get_all_users():
    ls_users = list(map(lambda x: {"user_type": USER_DICT_REVERSE.get(x["user_type"]),
                                   "insert_datetime": x["insert_datetime"].strftime("%Y-%m-%d %H:%M:%S"),
                                   "u_id": x["u_id"], "name": x["name"]},
                        get_user()))
    return ls_users


def delete_user_by_uid(u_id: Union[list, str]):
    res = delete_user(u_id=u_id)
    if res == "unsuccessful":
        raise HTTPException(status_code=400, detail="Something went wrong, please check u_id.")
    else:
        return res


def add_users_by_file(f_users: str):
    # TODO: ensure the robustness, columns type, names
    df = pd.read_excel(f_users).rename(columns=COLUMNS)
    # check columns
    if set(df.columns.tolist()) == set(COLUMNS.values()):
        df[['u_id', 'code']] = df[['u_id', 'code']].astype('str')
        df["user_type"] = df["user_type"].apply(lambda x: USER_DICT.get(x))
        df["insert_datetime"] = datetime.utcnow()
        return insert_users(df.to_dict('records'))
    else:
        HTTPException(status_code=400, detail="Columns do not fit for restriction.")


def revise_instruments():
    pass


def revise_consumables():
    pass


def delete_instruments():
    pass


def delete_consumables():
    pass


def add_instruments():
    pass


def add_consumables():
    pass


def get_surgery():
    pass
