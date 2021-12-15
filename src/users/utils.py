from enum import Enum
from typing import Optional


userdata = {
    1: {'id': 1, 'username': 'JonDoe', 'password': 'hasgcjbahyuwei'},
    2: {'id': 2, 'username': 'KateRin', 'password': 'hasgcjbahyuwei'},
    3: {'id': 3, 'username': 'Clint', 'password': 'hasgcjbahyuwei'},
}

class Roles(str, Enum):
    admin = "ADMIN"
    staff = "STAFF"
    superuser = "SUPERUSER"


class FakeUserDatabase:

    def get(self, id: Optional[int] = None, username: 
             Optional[str] = None):
        if id == None and username == None:
            raise Exception("Method 'get' received no params.")
        if id and username:
            user = userdata.get(id)
            if user and username == user['username']:
                return user
        elif id:
            return userdata.get(id)
        else:
            for _, user in userdata.items():
                if username == user['username']:
                    return user
        return None