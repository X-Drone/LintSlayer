from typing import Callable
from domain.entities import Project
from domain.services.project_service import ProjectService as ProjectDomainService
from ..use_cases.project_operations import DeleteProjectUseCase
from ..interfaces.uow import IUnitOfWork
from ..use_cases.create_project import CreateProjectUseCase
from ..dtos import RepoSource


class ProjectService:
    """Application service для управления проектами (Clean Architecture)"""
    
    def __init__(self,
                 create_project_uc: CreateProjectUseCase,
                 delete_project_uc: DeleteProjectUseCase,
                 domain_service: ProjectDomainService,
                 uow: IUnitOfWork):
        self.create_project_uc = create_project_uc
        self.delete_project_uc = delete_project_uc
        self.domain_service = domain_service
        self.uow = uow

    def create_project(self, owner: str, name: str, repo: RepoSource) -> Project:
        """Создает новый проект"""
        return self.create_project_uc(owner, name, repo)

    def get_user_projects(self, owner: str) -> list[Project]:
        """Получает проекты пользователя"""
        with self.uow:
            return self.uow.projects.getUserProjects(owner)

    def delete_project(self, project_id: int) -> None:
        """Удаляет проект"""
        return self.delete_project_uc(project_id)

    def get_project(self, project_id: int) -> Project | None:
        """Получает проект по ID"""
        with self.uow:
            return self.uow.projects.getById(project_id)
