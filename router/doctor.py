from fastapi import APIRouter, Depends

from core.backend.doctor import general_statistics, surgery_by_type, surgery_by_time
from core.backend.doctor_dashboard import get_general_data_by_month, get_surgery_time_series, get_contribution_matrix, \
    get_surgery_by_date
from core.backend.user import auth
from model.doctor import Doctor

router = APIRouter(prefix="/doctor")


@router.post('/general_statistics', tags=['Doctor'])
def get_general_statistics_api(u_id: str):
    return general_statistics(u_id=u_id)


@router.post('/get_surgery_by_type', tags=['Doctor'])
def get_surgery_by_type_api(u_id: str):
    return surgery_by_type(u_id=u_id)


@router.post('/get_surgery_by_time', tags=['Doctor'])
def get_surgery_by_time_api(u_id: str):
    return surgery_by_time(u_id=u_id)


@router.post('/get_general_data', tags=['Doctor'])
def get_general_data(doctor: Doctor):
    return get_general_data_by_month(surgeon_id=doctor.u_id, begin_time=doctor.begin_time, end_time=doctor.end_time)


@router.post('/get_surgery_time_series', tags=['Doctor'])
def get_surgery_time_series_api(doctor: Doctor):
    return get_surgery_time_series(surgeon_id=doctor.u_id, mode=doctor.mode)


@router.post('/get_doctor_contribution', tags=['Doctor'])
def get_doctor_contribution(u_id: str):
    return get_contribution_matrix(surgeon_id=u_id)


@router.post('/get_surgery_by_date', tags=['Doctor'])
def get_surgery_by_date_api(doctor: Doctor):
    return get_surgery_by_date(surgeon_id=doctor.u_id, date=doctor.date)


