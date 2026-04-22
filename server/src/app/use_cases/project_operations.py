from domain.entities import Project
from ..interfaces.repo_manager import IRepoManager
from ..interfaces.uow import IUnitOfWork


class GetUserProjectsUseCase:
    """Use case для получения проектов пользователя"""
    
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def __call__(self, owner: str) -> list[Project]:
        """Получает все проекты пользователя"""
        with self.uow:
            return self.uow.projects.getUserProjects(owner)


class DeleteProjectUseCase:
    """Use case для удаления проекта"""
    
    def __init__(self,
                 repo_manager: IRepoManager,
                 uow: IUnitOfWork):
        self.repo_manager = repo_manager
        self.uow = uow


    def __call__(self, project_id: int) -> None:
        """Удаляет проект по ID"""
        with self.uow:
            project = self.uow.projects.getById(project_id)
            if project:
                self.repo_manager.deleteRepo(project.repo_path)
                self.uow.projects.delete(project_id)
            else:
                raise ValueError(f"Project with id {project_id} not found")
