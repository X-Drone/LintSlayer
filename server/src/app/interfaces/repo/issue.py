from abc import ABC, abstractmethod
from domain.entities import Issue


class IIssueRepo(ABC):
    @abstractmethod
    def add(self, issue: Issue): ...

    @abstractmethod
    def add_many(self, issues: list[Issue]): ...
    
    @abstractmethod
    def getById(self, id: int) -> Issue: ...
    
    @abstractmethod
    def getAnalysisRunIssues(self, run_id: int) -> list[Issue]: ...
