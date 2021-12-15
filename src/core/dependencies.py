import time
from typing import Optional
from fastapi import Cookie, status, Request
from fastapi.exceptions import HTTPException

async def get_current_user():
    return {'logged_in_user': 'RohitPatil18'}


class CommonQueryParameters:
    def __init__(self, skip: int = 0, limit: int = 100):
        self.skip = skip
        self.limit = limit


async def check_session(sessionid: Optional[str] = Cookie(None)):
    if not sessionid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Session.')
    print(f'Session ID: {sessionid}')


async def yield_dependency(request: Request):
    try:
        print("Yield Statement.")
        yield True
    finally:
        print("After request completed.")