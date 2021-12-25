from typing import List, Optional
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

from core.dependencies import CommonQueryParameters, yield_dependency
from auth.dependencies import get_current_user

from users.utils import userdata, Roles
from users.schema import User, UserInfo


router = APIRouter(
    prefix="/users",
    tags=['User']
)


@router.get("/", response_model=List[User])
async def get_users_list(query: CommonQueryParameters = Depends()):
    userslist = [user for _, user in userdata.items()]
    return userslist[query.skip:query.limit]


@router.post("/", response_model=User, 
          response_model_exclude={"password"},
          status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    return user


@router.patch('/{user_id}', response_model=UserInfo)
async def partial_update_user(user: User, user_id: int):
    current_data = userdata.get(user_id)
    current_user_model = User(**current_data)
    if not current_data:
        raise HTTPException(status_code=404, detail="User not found")
    updated_data = user.dict(exclude_unset=True)
    user = current_user_model.copy(update=updated_data)
    userdata[user_id] = jsonable_encoder(user)
    return user


@router.get("/params/{user_id}/{user_name}")
async def check_params(
    user_id: int, user_name: str, role: Roles, 
    checkin: Optional[bool] = False,
    flag: bool = Depends(yield_dependency)
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


@router.get("/me", response_model=UserInfo)
async def loggedin_user_info(
    user: dict = Depends(get_current_user)
):
    return UserInfo(**user)