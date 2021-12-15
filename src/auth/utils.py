from typing import Optional
from datetime import timedelta, datetime

from jose import JWTError, jwt


SECRET_KEY = "6472378rcbwhjwiuei87492378hwisjasdfbjsvn873492"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(
    payload: dict, expire_mins: Optional[int] = ACCESS_TOKEN_EXPIRE_MINUTES
):
    expire_aft = datetime.utcnow() + timedelta(minutes=expire_mins)
    payload.update({"exp": expire_aft})
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token
