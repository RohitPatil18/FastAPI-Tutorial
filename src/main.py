import random
from enum import Enum
from typing import Optional, List

from fastapi import (
    FastAPI, Query, Path, Body, Cookie, Header)
from fastapi.param_functions import File
from pydantic import BaseModel, Field


app = FastAPI()

class Roles(str, Enum):
    admin = "ADMIN"
    staff = "STAFF"
    superuser = "SUPERUSER"


class Tag(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., min_length=1, max_length=100)

class Client(BaseModel):
    id: int = Field(..., ge=1)
    client_name: str = Field(..., min_length=1, max_length=200)


class Project(BaseModel):
    project_name: str = Field(..., min_length=1, max_length=200)
    clients: Optional[List[Client]]
    tags: List[str] = []


class Product(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=200)
    price: float = Field(..., ge=1, lt=100000)
    tax: Optional[int] = Field(5, ge=0, le=100)

class UserBase(BaseModel):
    id: int = Field(..., ge=1, le=99999)
    username: str = Field(..., min_length=10, max_length=50)

class UserInfo(UserBase):
    pass

class User(UserBase):
    password: str

class MetaOut(BaseModel):
    session_id: Optional[str]
    csrftoken: Optional[str]
    user_agent: Optional[str]
    language: Optional[str]
    x_token: Optional[str]

class GreetingOut(BaseModel):
    message: str
    meta: MetaOut


@app.get("/")
async def index():
    return {"message": "Hello world!"}


@app.get("/greet/{username}", response_model=GreetingOut,
        response_model_exclude_none=True)
async def greetings(
    username: str, 
    sessionid: Optional[str] = Cookie(None),
    csrftoken: Optional[str] = Cookie(None),
    user_agent: Optional[str] = Header(None),
    accept_language: Optional[str] = Header(None),
    x_token: Optional[str] = Header(None)
):
    return {
        "message": f"Hello, {username}!",
        "meta": {
            "session_id": sessionid,
            "csrftoken": csrftoken,
            "user_agent": user_agent,
            "language": accept_language,
            "x_token": x_token
        }
    }


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
    id: int, user: UserInfo, product: Product, commit: Optional[bool] = Body(True)
):
    return {
        "id": id,
        "product": product,
        "user": user,
        "committed": commit
    }


@app.post("/tags/")
async def create_tags(tags: List[Tag]):
    return tags


@app.post("/projects/")
async def create_projects(project: Project):
    response_data = {"id": random.randint(1, 99999)}
    response_data.update(**project.dict())
    return response_data


@app.post("/users/", response_model=User, 
          response_model_exclude={"password"})
async def create_user(user: User):
    return user