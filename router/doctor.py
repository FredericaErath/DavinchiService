from fastapi import APIRouter, Depends

from core.backend.doctor import general_statistics, surgery_by_type, surgery_by_time
from core.backend.user import auth

router = APIRouter(prefix="doctor")


@router.post('/general_statistics', tags=['Doctor'], dependencies=[Depends(auth.decode_token)])
def get_general_statistics_api(u_id: str):
    return general_statistics(u_id=u_id)


@router.post('/get_surgery_by_type', tags=['Doctor'], dependencies=[Depends(auth.decode_token)])
def get_surgery_by_type_api(u_id: str):
    return surgery_by_type(u_id=u_id)


@router.post('/get_surgery_by_time', tags=['Doctor'], dependencies=[Depends(auth.decode_token)])
def get_surgery_by_time_api(u_id: str):
    return surgery_by_time(u_id=u_id)


