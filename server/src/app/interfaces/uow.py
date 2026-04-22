from abc import ABC, abstractmethod
from .repo import IProjectRepo, IAnalysisRunRepo, IIssueRepo


class IUnitOfWork(ABC):
    projects: IProjectRepo
    runs: IAnalysisRunRepo
    issues: IIssueRepo

    def __enter__(self) -> "IUnitOfWork":
        return self
    
    def __exit__(self, exc_type, exc, tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()

    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def rollback(self) -> None: ...
