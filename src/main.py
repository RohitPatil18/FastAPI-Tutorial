import random
from enum import Enum
from typing import Optional, List

from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel


app = FastAPI()

class Roles(str, Enum):
    admin = "ADMIN"
    staff = "STAFF"
    superuser = "SUPERUSER"

class Product(BaseModel):
    product_name: str
    price: float
    tax: Optional[int] = 10

class User(BaseModel):
    id: int
    username: str


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


@app.get('/validators/params/{id}')
async def validate_params(
    *,
    q: str = Query(
        ..., min_length=5, max_length=10, title="Query",
        description="Query for any word."),
    query_fields: List[str] = Query(None, alias='query-fields'),
    page_size: int,
    id: int = Path(..., gt=0, le=100)
):
    query_field = query_fields if query_fields else '__all__'
    response_data = {
        'q': q, 
        'query-fields': query_field, 
        'length': page_size,
        'id': id    
    }
    return response_data


@app.post("/{category_id}/products/")
async def create_product(
    *,
    product: Product = Body(..., embed=True),
    category_id: int,
    draft: Optional[bool] = True
):
    total_tax = product.price * product.tax / 100 
    response_data = {
        "id": random.randint(1, 99999),
        "product_name": product.product_name,
        "category_id": category_id, 
        "price": product.price,
        "total_tax": total_tax,
        "total_cost": product.price + total_tax,
        "is_active": not draft
    }
    return response_data


@app.put("/products/{id}")
async def update_product(
    id: int, user: User, product: Product, commit: Optional[bool] = Body(True)
):
    return {
        "id": id,
        "product": product,
        "user": user,
        "committed": commit
    }