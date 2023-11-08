from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel


class Doctor(BaseModel):
    u_id: str
    begin_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    mode: Optional[str] = None
    date: Optional[datetime] = None


