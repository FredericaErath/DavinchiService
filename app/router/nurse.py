from fastapi import APIRouter, Depends

from core.backend.nurse import insert_surgery_info, get_instrument_ls, get_surgery_names, get_consumable_stock
from core.backend.surgery import insert_surgery_user
from app.core.backend.user import auth
from model.surgery import SurgeryInsert, SurgeryUpdate

router = APIRouter(prefix="/nurse")


@router.get('/get_surgery_name', tags=['Nurse'], dependencies=[Depends(auth.decode_token)])
def get_surgery_name_api():
    return get_surgery_names()


@router.post('/get_consumable_stock', tags=['Nurse'], dependencies=[Depends(auth.decode_token)])
def get_surgery_name_api(instruments: list):
    return get_consumable_stock(instruments=instruments)


@router.post('/get_instrument_ls', tags=['Nurse'], dependencies=[Depends(auth.decode_token)])
def get_instrument_ls_api(s_name: str):
    return get_instrument_ls(s_name=s_name)


@router.post('/add_surgery', tags=["Nurse"], dependencies=[Depends(auth.decode_token)])
def insert_surgery_api(surgery: SurgeryInsert):
    return insert_surgery_info(ls_c_name=surgery.ls_c_name,
                               ls_i_id=surgery.ls_i_id,
                               p_name=surgery.p_name,
                               admission_number=surgery.admission_number,
                               department=surgery.department,
                               s_name=surgery.s_name,
                               chief_surgeon=surgery.chief_surgeon,
                               associate_surgeon=surgery.associate_surgeon,
                               instrument_nurse=surgery.instrument_nurse,
                               circulating_nurse=surgery.circulating_nurse,
                               begin_time=surgery.begin_time,
                               end_time=surgery.end_time)


@router.post("/insert_surgery_user", tags=['Nurse'])
def insert_surgery_user_api(surgery: SurgeryUpdate):
    return insert_surgery_user(begin_time=surgery.begin_time, end_time=surgery.end_time, p_name=surgery.p_name,
                               date=surgery.date, admission_number=surgery.admission_number,
                               department=surgery.department, s_name=surgery.s_name,
                               chief_surgeon=surgery.chief_surgeon, associate_surgeon=surgery.associate_surgeon,
                               instrument_nurse=surgery.instrument_nurse, circulating_nurse=surgery.circulating_nurse,
                               instruments=surgery.instruments, consumables=surgery.consumables)
