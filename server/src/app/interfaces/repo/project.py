from abc import ABC, abstractmethod
from domain.entities import Project


class IProjectRepo(ABC):
    @abstractmethod
    def add(self, project: Project): ...
    
    @abstractmethod
    def getById(self, id: int) -> Project: ...
    
    @abstractmethod
    def getUserProjects(self, user: str) -> list[Project]: ...
    
    @abstractmethod
    def delete(self, id: int): ...
