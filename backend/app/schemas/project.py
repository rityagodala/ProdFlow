from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.user import UserResponse
from app.schemas.task import TaskResponse


class ProjectCreate(BaseModel):
    """Project creation schema."""

    name: str
    description: Optional[str] = None


class ProjectUpdate(BaseModel):
    """Project update schema."""

    name: Optional[str] = None
    description: Optional[str] = None


class ProjectResponse(BaseModel):
    """Project response schema."""

    id: int
    name: str
    description: Optional[str]
    owner_id: int
    owner: UserResponse
    created_at: datetime
    updated_at: Optional[datetime]
    tasks: list[TaskResponse] = []

    class Config:
        from_attributes = True

