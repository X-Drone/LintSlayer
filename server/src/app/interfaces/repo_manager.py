from abc import ABC, abstractmethod
from pathlib import Path


class IRepoManager(ABC):
    @abstractmethod
    def getBaseTempDir(self) -> Path: ...

    @abstractmethod
    def downloadRepo(self, owner: str, name: str, repo_url: str, timeout: int) -> Path: ...


    @abstractmethod
    def saveTempFile(self, owner: str, name: str, ext: str, content: str) -> Path: ...


    @abstractmethod
    def deleteRepo(self, path: Path): ...
