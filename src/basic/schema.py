from typing import Optional
from pydantic import BaseModel, Field


class Tag(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., min_length=1, max_length=100)


class MetaOut(BaseModel):
    session_id: Optional[str]
    csrftoken: Optional[str]
    user_agent: Optional[str]
    language: Optional[str]
    x_token: Optional[str]


class GreetingOut(BaseModel):
    message: str
    meta: MetaOut
