from sqlalchemy.orm import Session
from typing import List

from app.core.exceptions import NotFoundError, ForbiddenError
from app.models.task import Task
from app.models.project import Project
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """Task service."""

    @staticmethod
    def get_tasks(db: Session, project_id: int, user_id: int) -> List[Task]:
        """Get all tasks for a project."""
        # Verify project ownership
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NotFoundError("Project", str(project_id))
        if project.owner_id != user_id:
            raise ForbiddenError("You don't have permission to access this project")
        return db.query(Task).filter(Task.project_id == project_id).all()

    @staticmethod
    def get_task(db: Session, task_id: int, project_id: int, user_id: int) -> Task:
        """Get a task by ID."""
        task = db.query(Task).filter(Task.id == task_id, Task.project_id == project_id).first()
        if not task:
            raise NotFoundError("Task", str(task_id))
        # Verify project ownership
        project = db.query(Project).filter(Project.id == project_id).first()
        if project.owner_id != user_id:
            raise ForbiddenError("You don't have permission to access this task")
        return task

    @staticmethod
    def create_task(
        db: Session, project_id: int, task_data: TaskCreate, user_id: int
    ) -> Task:
        """Create a new task."""
        # Verify project ownership
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NotFoundError("Project", str(project_id))
        if project.owner_id != user_id:
            raise ForbiddenError("You don't have permission to create tasks in this project")

        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            project_id=project_id,
            assignee_id=task_data.assignee_id,
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def update_task(
        db: Session,
        task_id: int,
        project_id: int,
        task_data: TaskUpdate,
        user_id: int,
    ) -> Task:
        """Update a task."""
        task = TaskService.get_task(db, task_id, project_id, user_id)
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.status is not None:
            task.status = task_data.status
        if task_data.assignee_id is not None:
            task.assignee_id = task_data.assignee_id
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def delete_task(db: Session, task_id: int, project_id: int, user_id: int) -> None:
        """Delete a task."""
        task = TaskService.get_task(db, task_id, project_id, user_id)
        db.delete(task)
        db.commit()

