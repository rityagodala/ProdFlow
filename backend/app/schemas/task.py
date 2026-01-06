from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.task import TaskStatus
from app.schemas.user import UserResponse


class TaskCreate(BaseModel):
    """Task creation schema."""

    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    assignee_id: Optional[int] = None


class TaskUpdate(BaseModel):
    """Task update schema."""

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    assignee_id: Optional[int] = None


class TaskResponse(BaseModel):
    """Task response schema."""

    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    project_id: int
    assignee_id: Optional[int]
    assignee: Optional[UserResponse] = None
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

