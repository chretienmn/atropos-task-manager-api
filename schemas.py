from enum import Enum
from pydantic import BaseModel


# Request model for creating a task
class JobNameEnum(str, Enum):
    evidence = "evidence"


class CreateTaskRequest(BaseModel):
    job_name: JobNameEnum


# Response model for task creation
class CreateTaskResponse(BaseModel):
    task_id: str
    job_run_id: str


# Response model for task status
class TaskStatusResponse(BaseModel):
    task_id: str
    status: str


# Response model for task result
class TaskResultResponse(BaseModel):
    task_id: str
    result: dict
