from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel


class SurgeryInsert(BaseModel):
    ls_c_name: list
    ls_i_id: list
    p_name: str
    admission_number: int
    department: str
    s_name: str
    chief_surgeon: str
    associate_surgeon: str
    instrument_nurse: list
    circulating_nurse: list
    begin_time: datetime
    end_time: datetime


class SurgeryGet(BaseModel):
    page: Optional[int] = None
    limit_size: Optional[int] = 20
    begin_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    department: Union[str, list[str]] = None
    s_name: Union[str, list[str]] = None


class SurgeryUpdate(BaseModel):
    s_id: Optional[int] = None
    p_name: Optional[str] = None
    begin_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    date: Optional[datetime] = None
    admission_number: Optional[int] = None
    department: Optional[str] = None
    s_name: Optional[str] = None
    chief_surgeon: Optional[str] = None
    associate_surgeon: Optional[str] = None
    instrument_nurse: Optional[list] = None
    circulating_nurse: Optional[list] = None
    instruments: Optional[list] = None
    consumables: Optional[list] = None


class Contribution(BaseModel):
    df: list
    name: str
