from abc import ABC, abstractmethod
from domain.entities import AnalysisRun


class IAnalysisRunRepo(ABC):
    @abstractmethod
    def add(self, run: AnalysisRun): ...
    
    @abstractmethod
    def getById(self, id: int) -> AnalysisRun: ...

    @abstractmethod
    def update(self, run: AnalysisRun): ...
    
    @abstractmethod
    def getProjectRuns(self, project_id: int): ...
