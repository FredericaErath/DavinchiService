from typing import Optional, Union
from pydantic import BaseModel


class Instrument(BaseModel):
    i_id: Optional[Union[int, list[int]]]
    i_name: Optional[str]
    times: Optional[int]
