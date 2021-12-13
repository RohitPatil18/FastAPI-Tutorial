from enum import Enum
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Roles(str, Enum):
    admin = "ADMIN"
    staff = "STAFF"
    superuser = "SUPERUSER"

class Product(BaseModel):
    id: int
    product_name: str
    price: float
    tax: Optional[int] = 10


@app.get("/")
async def index():
    return {"message": "Hello world!"}


@app.get("/greet/{username}")
async def greetings(username: str):
    return {"message": f"Hello, {username}!"}


@app.get("/roles/{role}")
async def check_user(role: Roles):
    if role == Roles.admin:
        return {"message": "Can't connect to Admin."}
    elif role.value == Roles.staff.value:
        return {"message": "Staff will contact you."}
    else:
        return {"message": "Permission denied."}


@app.get("/params/{user_id}/{user_name}")
async def check_params(
    user_id: int, user_name: str, role: Roles, 
    checkin: Optional[bool] = False
):
    return {
        "id": user_id,
        "user_name": user_name,
        "role": role,
        "checkin": checkin 
    }


@app.post("/{category_id}/products/")
async def create_product(
    product: Product,
    category_id: int,
    draft: Optional[bool] = True
):
    total_tax = product.price * product.tax / 100 
    response_data = {
        "id": product.id,
        "product_name": product.product_name,
        "category_id": category_id, 
        "price": product.price,
        "total_tax": total_tax,
        "total_cost": product.price + total_tax,
        "is_active": not draft
    }
    return response_data