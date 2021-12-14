from enum import Enum


userdata = {
    1: {'id': 1, 'username': 'JonDoe', 'password': 'hasgcjbahyuwei'},
    2: {'id': 2, 'username': 'KateRin', 'password': 'hasgcjbahyuwei'},
    3: {'id': 3, 'username': 'Clint', 'password': 'hasgcjbahyuwei'},
}

class Roles(str, Enum):
    admin = "ADMIN"
    staff = "STAFF"
    superuser = "SUPERUSER"