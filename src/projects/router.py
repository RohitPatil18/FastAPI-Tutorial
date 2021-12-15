import time
import random
from fastapi import APIRouter, status, BackgroundTasks

from projects.schema import Project


router = APIRouter(
    prefix='/projects',
    tags=['Project']
)

def notify_clients(project: Project):
    clients = project.clients
    print("Background task received: notify_clients")
    for client in clients:
        time.sleep(3)
        print(f"{project.project_name} assigned to {client.client_name}")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_projects(
    project: Project, background_tasks: BackgroundTasks
):
    response_data = {"id": random.randint(1, 99999)}
    response_data.update(**project.dict())
    background_tasks.add_task(notify_clients, project)
    return response_data
