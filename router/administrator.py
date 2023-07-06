import os
from typing import Union

from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks

from core.backend.administrator import get_all_users, delete_user_by_uid, add_users_by_file
from core.backend.instrument import get_all_instrument, revise_instrument, add_instruments_by_file, add_one_instrument, \
    download_instrument_qr_code
from core.backend.user import register, revise_user_info
from model.user import User

router = APIRouter(prefix="/admin")


@router.post('/add_user', tags=['Admin'])
def add_user(user: User):
    return register(u_id=user.u_id, name=user.name, user_type=user.user_type, pwd=user.pwd)


@router.post('/revise_user', tags=['Admin'])
def revise_user(user: User):
    print(user)
    return revise_user_info(u_id=user.u_id, pwd=user.pwd, name=user.name, new_u_id=user.new_id)


@router.get('/get_user', tags=['Admin'])
def get_all_users_api():
    return get_all_users()


@router.post('/delete_user', tags=['Admin'])
def delete_user_api(u_id: Union[list, str]):
    return delete_user_by_uid(u_id=u_id)


@router.post("/upload_users", tags=['Admin'])
async def upload_users(file: UploadFile):
    file_upload = await file.read()
    file_name = 'temp.xlsx'
    f_out = open(f'{file_name}', 'xb')
    f_out.write(file_upload)
    res = add_users_by_file(file_name)
    f_out.close()
    task = BackgroundTasks()
    task.add_task(os.remove(file_name), file_name)
    return res


@router.get("/get_instruments", tags=['Admin'])
def get_instrument_api():
    return get_all_instrument()


@router.post("/revise_instruments", tags=['Admin'])
def revise_instrument_api(i_id: int,
                          times: int):
    return revise_instrument(i_id=i_id, times=times)


@router.post("/add_instrument", tags=['Admin'])
async def add_instrument(i_name: str, times: int = None):
    res = add_one_instrument(i_name=i_name, times=times)
    return FileResponse(res)


@router.post("/upload_instruments", tags=['Admin'])
async def upload_instruments(file: UploadFile):
    file_upload = await file.read()
    file_name = 'temp.xlsx'
    f_out = open(f'{file_name}', 'xb')
    f_out.write(file_upload)
    res = add_instruments_by_file(file_name)
    f_out.close()
    task = BackgroundTasks()
    task.add_task(os.remove(file_name), file_name)
    return FileResponse(res)


@router.post("/download_instrument_qrcode", tags=['Admin'])
async def download_qrcode(i_id: int):
    res = download_instrument_qr_code(i_id=i_id)
    return FileResponse(res)
