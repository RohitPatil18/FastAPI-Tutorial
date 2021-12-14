from typing import Optional
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

from users.utils import userdata, Roles
from users.schema import User, UserInfo


router = APIRouter(
    prefix="/users",
    tags=['User']
)


@router.get("/params/{user_id}/{user_name}")
async def check_params(
    user_id: int, user_name: str, role: Roles, 
    checkin: Optional[bool] = False
):
    """
    Simple endpoint which takes URL parameters and Query 
    Parameters and return them in Response.
    """
    return {
        "id": user_id,
        "user_name": user_name,
        "role": role,
        "checkin": checkin 
    }


@router.post("/", response_model=User, 
          response_model_exclude={"password"},
          status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    return user


@router.patch('/users/{user_id}', response_model=UserInfo)
async def partial_update_user(user: User, user_id: int):
    current_data = userdata.get(user_id)
    current_user_model = User(**current_data)
    if not current_data:
        raise HTTPException(status_code=404, detail="User not found")
    updated_data = user.dict(exclude_unset=True)
    user = current_user_model.copy(update=updated_data)
    userdata[user_id] = jsonable_encoder(user)
    return user