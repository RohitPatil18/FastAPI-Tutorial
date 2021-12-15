from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.exceptions import AuthenticationFailed
from users.utils import FakeUserDatabase
from users.schema import UserInfo

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post('/login/')
async def auth_login(form: OAuth2PasswordRequestForm = Depends()):
    db = FakeUserDatabase()
    user = db.get(username=form.username)
    if not user or user['password'] != form.password:
        raise AuthenticationFailed(message="Invalid credentials.")
    return {
        "access_token": f"verified_{user['username']}",
        "token_type": "Bearer",
        "user": UserInfo(**user)
    }