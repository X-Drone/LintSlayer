from ..values import Status
from datetime import datetime, UTC


class AnalysisRun:
    id: int | None
    project_id: int
    status: Status
    timestamp: datetime | None
    
    def __init__(self,
                 id: int | None,
                 project_id: int,
                 status: Status,
                 timestamp: datetime | None
            ) -> None:
        self.id = id
        self.project_id = project_id
        self.status = status
        self.timestamp = timestamp
    
    @staticmethod
    def create(project_id: int
            ) -> "AnalysisRun":
        return AnalysisRun(None,
                       project_id,
                       Status.PENDING,
                       None)

    def run(self) -> None:
        if self.status != Status.PENDING:
            raise Exception("Invalid state")
        self.status = Status.RUNNING

    def complete(self, status: Status) -> None:
        if self.status != Status.RUNNING:
            raise Exception("Invalid state")
        self.status = status
        self.timestamp = datetime.now(UTC)
