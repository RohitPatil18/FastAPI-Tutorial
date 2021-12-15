from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.exceptions import AuthenticationFailed
from users.utils import FakeUserDatabase
from users.schema import UserInfo

from .utils import create_access_token
from .schema import AuthToken


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post('/login/', response_model=AuthToken)
async def auth_login(form: OAuth2PasswordRequestForm = Depends()):
    db = FakeUserDatabase()
    user = db.get(username=form.username)
    if not user or user['password'] != form.password:
        raise AuthenticationFailed(message="Invalid credentials.")
    del user["password"]
    token = create_access_token(user)
    return AuthToken(access_token=token, user=user)