"""
Generic functions for all users
"""
from typing import Optional

from fastapi import HTTPException

from constant import USER_DICT
from core.database import update_user, get_user, insert_user
from core.backend.auth import AuthHandler

auth = AuthHandler()


def revise_user_info(u_id: str,
                     pwd: str = None,
                     name: str = None,
                     new_u_id: str = None):
    """
    Revise user info.
    """
    if pwd is not None:
        pwd = auth.get_pwd_hash(pwd=pwd)
    res = update_user(u_id=u_id, pwd=pwd, name=name, new_id=new_u_id)
    if res == "unsuccessful":
        raise HTTPException(status_code=400, detail="Update failure, please check your info.")
    else:
        return res


def get_user_type(u_id: str):
    """
    Get specific user's type.

    :param u_id: user's id
    :return: specific user's type
    """
    try:
        user = get_user(u_id=u_id)[0]
    except IndexError:
        return "failed"
    return user["user_type"]


def register(u_id: str, name: str, user_type: str, pwd: str):
    """Register one user."""
    if len(get_user(u_id=u_id)) != 0:
        raise HTTPException(status_code=400, detail="The user_id has been already taken")
    else:
        hashed_pwd = auth.get_pwd_hash(pwd=pwd)
    return insert_user(u_id=u_id, name=name, user_type=user_type, code=hashed_pwd)


def login(u_id: str, pwd: str):
    """User login."""
    try:
        user = get_user(u_id=u_id)[0]
    except IndexError:
        raise HTTPException(status_code=400, detail="Invalid userid")
    if auth.verify_pwd(pwd, user["code"]) is False:
        raise HTTPException(status_code=400, detail="Invalid password")
    else:
        token = auth.encode_token(user_id=u_id)
        return {"token": token, "user_type": user["user_type"], "name": user["name"], "u_id": user["u_id"]}
