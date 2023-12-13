from fastapi import APIRouter, Depends

from core.backend.doctor import get_general_data_by_month, get_surgery_time_series, get_contribution_matrix, \
    get_surgery_by_date, send_message, get_message_by_uid
from core.backend.user import auth
from model.doctor import Doctor

router = APIRouter(prefix="/doctor")


@router.post('/get_general_data', tags=['Doctor'], dependencies=[Depends(auth.decode_token)])
def get_general_data(doctor: Doctor):
    return get_general_data_by_month(surgeon_id=doctor.u_id, begin_time=doctor.begin_time, end_time=doctor.end_time)


@router.post('/get_surgery_time_series', tags=['Doctor'], dependencies=[Depends(auth.decode_token)])
def get_surgery_time_series_api(doctor: Doctor):
    return get_surgery_time_series(surgeon_id=doctor.u_id, mode=doctor.mode)


@router.post('/get_doctor_contribution', tags=['Doctor'], dependencies=[Depends(auth.decode_token)])
def get_doctor_contribution(doctor: Doctor):
    return get_contribution_matrix(surgeon_id=doctor.u_id)


@router.post('/get_surgery_by_date', tags=['Doctor'], dependencies=[Depends(auth.decode_token)])
def get_surgery_by_date_api(doctor: Doctor):
    return get_surgery_by_date(surgeon_id=doctor.u_id, date=doctor.date)


@router.post('/send_message', tags=['Doctor'], dependencies=[Depends(auth.decode_token)])
def send_message_api(doctor: Doctor):
    return send_message(u_id=doctor.u_id, u_name=doctor.u_name, message=doctor.message)


@router.post("/get_message", tags=['Admin'], dependencies=[Depends(auth.decode_token)])
def get_message(doctor: Doctor):
    return get_message_by_uid(u_id=doctor.u_id)
