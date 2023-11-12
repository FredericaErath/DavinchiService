from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel


class Doctor(BaseModel):
    u_id: str
    u_name: Optional[str] = None
    message: Optional[str] = None
    begin_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    mode: Optional[str] = None
    date: Optional[datetime] = None


class Message(BaseModel):
    m_id: Optional[int] = None
    status: Optional[Union[str, list[str]]] = None
    priority: Optional[Union[str, list[str]]] = None
    begin_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    feedback: Optional[str] = None


