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
    part: str


class SurgeryGet(BaseModel):
    begin_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    department: Union[str, list[str]] = None
    s_name: Union[str, list[str]] = None
