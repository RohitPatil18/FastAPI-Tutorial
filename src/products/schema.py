from typing import Optional
from pydantic import BaseModel, Field


class Product(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=200)
    price: float = Field(..., ge=1, lt=100000)
    tax: Optional[int] = Field(5, ge=0, le=100)
