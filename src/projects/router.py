import random
from fastapi import APIRouter, status

from projects.schema import Project


router = APIRouter(
    prefix='/projects',
    tags=['Project']
)

@router.post("/projects/", status_code=status.HTTP_201_CREATED)
async def create_projects(project: Project):
    response_data = {"id": random.randint(1, 99999)}
    response_data.update(**project.dict())
    return response_data
