from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Surgery(BaseModel):
    ls_c_name: list
    ls_i_id: list
    p_name: str
    admission_number: int
    department: str
    s_name: str
    chief_surgeon: str
    associate_surgeon: str
    instrument_nurse: str
    circulating_nurse: str
    begin_time: datetime
    end_time: datetime
    part: str
