from pydantic import BaseModel, Field


class UserBase(BaseModel):
    id: int = Field(..., ge=1, le=99999)
    username: str = Field(..., min_length=5, max_length=50)

class UserInfo(UserBase):
    pass

class User(UserBase):
    password: str = None
