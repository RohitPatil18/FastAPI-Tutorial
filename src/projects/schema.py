from typing import Optional, List
from pydantic import BaseModel, Field


class Client(BaseModel):
    id: int = Field(..., ge=1)
    client_name: str = Field(..., min_length=1, max_length=200)


class Project(BaseModel):
    project_name: str = Field(..., min_length=1, max_length=200)
    clients: Optional[List[Client]]
    tags: List[str] = []