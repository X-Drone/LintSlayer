from abc import ABC, abstractmethod
from pathlib import Path


class IRepoManager(ABC):
    @abstractmethod
    def downloadRepo(self, repo_url: str, timeout: int) -> Path: ...


    @abstractmethod
    def saveTempFile(self, ext: str, content: str) -> Path: ...


    @abstractmethod
    def deleteRepo(self, path: Path): ...
