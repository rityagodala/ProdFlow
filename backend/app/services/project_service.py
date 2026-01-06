from sqlalchemy.orm import Session
from typing import List

from app.core.exceptions import NotFoundError, ForbiddenError
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    """Project service."""

    @staticmethod
    def get_projects(db: Session, user_id: int) -> List[Project]:
        """Get all projects for a user."""
        return db.query(Project).filter(Project.owner_id == user_id).all()

    @staticmethod
    def get_project(db: Session, project_id: int, user_id: int) -> Project:
        """Get a project by ID."""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NotFoundError("Project", str(project_id))
        if project.owner_id != user_id:
            raise ForbiddenError("You don't have permission to access this project")
        return project

    @staticmethod
    def create_project(db: Session, project_data: ProjectCreate, user_id: int) -> Project:
        """Create a new project."""
        project = Project(
            name=project_data.name,
            description=project_data.description,
            owner_id=user_id,
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def update_project(
        db: Session, project_id: int, project_data: ProjectUpdate, user_id: int
    ) -> Project:
        """Update a project."""
        project = ProjectService.get_project(db, project_id, user_id)
        if project_data.name is not None:
            project.name = project_data.name
        if project_data.description is not None:
            project.description = project_data.description
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def delete_project(db: Session, project_id: int, user_id: int) -> None:
        """Delete a project."""
        project = ProjectService.get_project(db, project_id, user_id)
        db.delete(project)
        db.commit()

