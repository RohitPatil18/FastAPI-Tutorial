from typing import Optional, List
from fastapi import (
    APIRouter, Query, Path, Cookie, Header, Response, 
    status, UploadFile, Form, File)

from core.exceptions import AuthenticationFailed
from .schema import GreetingOut, Tag


router = APIRouter(
    tags=['Common']
)


@router.get("/", deprecated=True)
async def index():
    return {"message": "Hello world!"}


@router.get("/greet/{username}", response_model=GreetingOut,
        response_model_exclude_none=True)
async def greetings(
    username: str, 
    sessionid: Optional[str] = Cookie(None),
    csrftoken: Optional[str] = Cookie(None),
    user_agent: Optional[str] = Header(None),
    accept_language: Optional[str] = Header(None),
    x_token: Optional[str] = Header(None)
):
    return {
        "message": f"Hello, {username}!",
        "meta": {
            "session_id": sessionid,
            "csrftoken": csrftoken,
            "user_agent": user_agent,
            "language": accept_language,
            "x_token": x_token
        }
    }


@router.get('/validators/params/{id}')
async def validate_params(
    *,
    q: str = Query(
        ..., min_length=5, max_length=10, title="Query",
        description="Query for any word."),
    query_fields: List[str] = Query(None, alias='query-fields'),
    page_size: int,
    id: int = Path(..., gt=0, le=100)
):
    query_field = query_fields if query_fields else '__all__'
    response_data = {
        'q': q, 
        'query-fields': query_field, 
        'length': page_size,
        'id': id    
    }
    return response_data


@router.post("/tags/", status_code=status.HTTP_201_CREATED)
async def create_tags(tags: List[Tag]):
    return tags


@router.post(
    "/login/",
    summary="Login endpoint which should return authentication token.", 
    response_description="Successful authentication message"
)
async def login(
    *, username: str = Form(...), password: str = Form(...),
    response: Response    
):
    """
    Login to application with following data

    - **username**: Username of a user used while signing up
    - **password**: A secret phrase/word used to protect account 
    """
    if username == 'admin' and password == 'admin':
        return {"message": "Login Successful."}
    raise AuthenticationFailed(message="Invalid Credentials")


@router.post('/uploadfiles/')
async def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type
    }

