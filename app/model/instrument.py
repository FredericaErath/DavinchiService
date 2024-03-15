from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel


class Instrument(BaseModel):
    i_id: Optional[Union[int, list[int]]] = None
    i_name: Optional[Union[str, list[str]]] = None
    times: Optional[Union[int, list[int]]] = None
    begin_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    validity: bool = None
