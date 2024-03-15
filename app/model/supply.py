from datetime import datetime
from typing import Union, Optional

from pydantic import BaseModel


class Supply(BaseModel):
    begin_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    c_id: Optional[Union[int, list[int]]] = None
    c_name: Optional[Union[str, list[str]]] = None
    description: Optional[Union[str, list[str]]] = None
    validity: Optional[bool] = None


class SupplyGet(BaseModel):
    c_name: str
    num: int


class SupplyRevise(BaseModel):
    c_id: int
    description: str
