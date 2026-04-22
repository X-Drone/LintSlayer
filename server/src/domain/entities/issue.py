from pathlib import Path
from ..values import Severity


class Issue:
    id: int | None
    run_id: int
    file_path: Path
    line_start: int
    line_end: int
    severity: Severity
    message: str
    
    def __init__(self,
                 id: int | None,
                 run_id: int,
                 file_path: Path,
                 line_start: int,
                 line_end: int,
                 severity: Severity,
                 message: str
            ) -> None:
        self.id = id
        self.run_id = run_id
        self.file_path = file_path
        self.line_start = line_start
        self.line_end = line_end
        self.severity = severity
        self.message = message
    
    @staticmethod
    def create(run_id: int,
               file_path: Path,
               line_start: int,
               line_end: int,
               severity: Severity,
               message: str
            ) -> "Issue":
        return Issue(None,
                     run_id,
                     file_path,
                     line_start,
                     line_end,
                     severity,
                     message)
