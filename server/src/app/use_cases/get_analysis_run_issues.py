from typing import Protocol
from domain.entities import Issue
from ..interfaces.uow import IUnitOfWork


class IGetAnalysisRunIssuesUseCase(Protocol):
    def __call__(self, run_id: int) -> list[Issue]:
        ...


class GetAnalysisRunIssuesUseCase:
    """Use case для получения результатов анализа"""
    
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow


    def __call__(self, run_id: int) -> list[Issue]:
        """Получает проект по ID"""
        with self.uow:
            return self.uow.issues.getAnalysisRunIssues(run_id)
