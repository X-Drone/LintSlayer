from abc import ABC, abstractmethod
from typing import Callable, List
from domain.entities import Issue
from .uow import IUnitOfWork


class IAnalyser(ABC):
    ext: str
    @abstractmethod
    def analyse(self, text: str, on_complete: Callable[[List[Issue], IUnitOfWork], None]): ...
