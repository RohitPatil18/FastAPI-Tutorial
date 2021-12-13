from enum import Enum
from fastapi import FastAPI

app = FastAPI()

class Roles(str, Enum):
    admin = "ADMIN"
    staff = "STAFF"
    superuser = "SUPERUSER"


@app.get("/")
async def index():
    return {"message": "Hello world!"}

@app.get("/greet/{username}")
async def greetings(username: str):
    return {"message": f"Hello, {username}!"}

@app.get("/roles/{role}")
async def check_user(role: Roles):
    if role == Roles.admin:
        return {"message": "Can't connect to Admin."}
    elif role.value == Roles.staff.value:
        return {"message": "Staff will contact you."}
    else:
        return {"message": "Permission denied."}