from typing import Optional, Union
from pydantic import BaseModel


class User(BaseModel):
    u_id: Union[list[str], str]
    name: Optional[str] = None
    user_type: Optional[str] = None
    pwd: Optional[str] = None
    new_id: Optional[str] = None
