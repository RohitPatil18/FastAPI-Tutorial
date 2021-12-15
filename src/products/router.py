import random
from typing import Optional
from fastapi import APIRouter, Body, status

from users.schema import UserInfo
from products.schema import Product


categories_router = APIRouter(
    prefix='/categories',
    tags=['Product', 'Category']
) 

products_router = APIRouter(
    prefix='/products',
    tags=['Product']
) 


@categories_router.post(
    "/{category_id}/products/", 
    status_code=status.HTTP_201_CREATED
)
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


@products_router.put("/{id}")
async def update_product(
    id: int, user: UserInfo, product: Product, 
    commit: Optional[bool] = Body(True)
):
    return {
        "id": id,
        "product": product,
        "user": user,
        "committed": commit
    }
