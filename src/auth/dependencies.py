
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from core.exceptions import AuthenticationFailed
from users.utils import FakeUserDatabase


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/")


def fake_decode_token(user_db: FakeUserDatabase, token: str):
    if not token:
        return None
    username = token.lstrip('verified_')
    user = user_db.get(username=username)
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_db: FakeUserDatabase = Depends()
):
    user = fake_decode_token(user_db, token)
    if not user:
        raise AuthenticationFailed
    return user