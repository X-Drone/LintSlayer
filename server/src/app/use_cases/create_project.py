from pathlib import Path
from typing import Protocol
from domain.entities import Project
from ..interfaces.uow import IUnitOfWork
from ..interfaces.repo_manager import IRepoManager
from ..dtos import RepoSource


class ICreateProjectUseCase(Protocol):
    def __call__(self, owner: str, repo: RepoSource) -> Project:
        ...


class CreateProjectUseCase:
    """Use case для создания проекта (application layer)"""
    
    def __init__(self,
                 repo_manager: IRepoManager,
                 uow: IUnitOfWork):
        self.repo_manager = repo_manager
        self.uow = uow


    def __call__(self, owner: str, name: str, repo: RepoSource) -> Project:
        """Создает новый проект по заданному источнику кода"""
        repo_path: Path = self._resolveRepo(repo)
        
        with self.uow:
            # Используем фабрику domain entity
            project = Project.create(owner, name, repo_path)
            self.uow.projects.add(project)
        
        return project


    def _resolveRepo(self, repo: RepoSource) -> Path:
        """Резолвит источник репозитория в путь"""
        from app.dtos import RepoFromUrl, RepoFromPath, RepoFromText
        
        if isinstance(repo, RepoFromUrl):
            return self.repo_manager.downloadRepo(repo.url, 15)
        
        if isinstance(repo, RepoFromPath):
            return repo.path
        
        if isinstance(repo, RepoFromText):
            return self.repo_manager.saveTempFile(repo.ext, repo.content)
        
        raise ValueError(f"Unsupported repo source: {type(repo)}")
