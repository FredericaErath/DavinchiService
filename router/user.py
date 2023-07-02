from fastapi import APIRouter, Depends
from core.backend.user import login, register, auth, revise_user_info
from model.user import User

router = APIRouter()


@router.post('/login', tags=["User"])
def login_api(user: User):
    return login(u_id=user.u_id, pwd=user.pwd)


@router.post('/register', tags=["User"])
def register_api(user: User):
    return register(u_id=user.u_id, pwd=user.pwd, user_type=user.user_type, name=user.name)


@router.post('/revise', dependencies=[Depends(auth.decode_token)], tags=["User"])
def revise_api(user: User):
    return revise_user_info(u_id=user.u_id, pwd=user.pwd, name=user.name, new_u_id=user.new_id)


@router.get('/protected', dependencies=[Depends(auth.decode_token)], tags=["User"])
def protected():
    return {"name": "1"}
