"""
Generic functions for all users
"""
import base64
from fastapi import HTTPException
from core.database import update_user, get_user, insert_user
from auth import AuthHandler


auth = AuthHandler()


def revise_user_info(code: str, u_id: str):
    """

    :param code:
    :param u_id:
    :return:
    """
    code = str(base64.b64encode(code.encode('utf-8')))[2:-1]
    return update_user(key="code", value=code, u_id=u_id)


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


def register(u_id: str, name: str, user_type: str, code: str):
    """Register one user."""
    if len(get_user(u_id=u_id)) != 0:
        raise HTTPException(status_code=400, detail="The user_id has been already taken")
    else:
        hashed_pwd = auth.get_pwd_hash(pwd=code)
    return insert_user(u_id=u_id, name=name, user_type=user_type, code=hashed_pwd)


def login(u_id: str, pwd: str):
    """User login."""
    try:
        user = get_user(u_id=u_id)[0]
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid userid")
    if auth.verify_pwd(pwd, user["code"]) is False:
        raise HTTPException(status_code=401, detail="Invalid password")
    else:
        token = auth.encode_token(user_id=u_id)
        return {"token": token}
