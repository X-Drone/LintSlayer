from typing import Protocol
from domain.entities import Project
from ..interfaces.uow import IUnitOfWork


class IGetProjectUseCase(Protocol):
    def __call__(self, project_id: int) -> Project | None:
        ...


class GetProjectUseCase:
    """Use case для получения информации о проекте"""
    
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow


    def __call__(self, project_id: int) -> Project | None:
        """Получает проект по ID"""
        with self.uow:
            return self.uow.projects.getById(project_id)
