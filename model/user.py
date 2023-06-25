from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    u_id: str
    name: Optional[str]
    user_type: Optional[str]
    pwd: str
