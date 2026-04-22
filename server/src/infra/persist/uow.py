from typing import Callable
from sqlalchemy.orm import Session
from app.interfaces.uow import IUnitOfWork
from .repo import ProjectRepo, AnalysisRunRepo, IssueRepo


class UnitOfWork(IUnitOfWork):
    session: Session | None
    get_session: Callable[[], Session]

    def __init__(self, get_session: Callable[[], Session]):
        self.get_session = get_session

    def __enter__(self) -> "IUnitOfWork":
        self.session = self.get_session()
        self.projects = ProjectRepo(self.session)
        self.runs = AnalysisRunRepo(self.session)
        self.issues = IssueRepo(self.session)
        return super().__enter__()
    
    def __exit__(self, exc_type, exc, tb):
        try:
            super().__exit__(exc_type, exc, tb)
        finally:
            if self.session:
                self.session.close()
                self.session = None

    def commit(self) -> None:
        if self.session:
            self.session.commit()

    def rollback(self) -> None:
        if self.session:
            self.session.rollback()
