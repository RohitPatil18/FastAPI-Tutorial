from typing import Optional
from pydantic import BaseModel
from users.schema import UserBase

class AuthToken(BaseModel):
    access_token: str
    token_type: Optional[str] = "Bearer"
    user: UserBase
