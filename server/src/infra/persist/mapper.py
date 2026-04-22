from domain.entities import Project, AnalysisRun, Issue
from domain.values import Status, Severity
from .models import Project as ProjectModel
from .models import AnalysisRun as AnalysisRunModel
from .models import Issue as IssueModel
from pathlib import Path

class ProjectMapper:
    @staticmethod
    def to_domain(model: ProjectModel) -> Project:
        return Project(
            id=model.id,
            owner=model.owner,
            name=model.name,
            repo_path=Path(model.repo_path)
        )

    @staticmethod
    def to_model(entity: Project) -> ProjectModel:
        return ProjectModel(
            id=entity.id,
            owner=entity.owner,
            name=entity.name,
            repo_path=str(entity.repo_path)
        )

class AnalysisRunMapper:
    @staticmethod
    def to_domain(model: AnalysisRunModel) -> AnalysisRun:
        return AnalysisRun(
            id=model.id,
            project_id=model.project_id,
            status=Status(model.status),
            timestamp=model.timestamp
        )

    @staticmethod
    def to_model(entity: AnalysisRun) -> AnalysisRunModel:
        return AnalysisRunModel(
            id=entity.id,
            project_id=entity.project_id,
            status=entity.status.value,
            timestamp=entity.timestamp
        )

class IssueMapper:
    @staticmethod
    def to_domain(model: IssueModel) -> Issue:
        return Issue(
            id=model.id,
            run_id=model.run_id,
            file_path=model.file_path,
            line_start=model.line_start,
            line_end=model.line_end,
            severity=Severity(model.severity),
            message=model.message
        )

    @staticmethod
    def to_model(entity: Issue) -> IssueModel:
        return IssueModel(
            id=entity.id,
            run_id=entity.run_id,
            file_path=entity.file_path,
            line_start=entity.line_start,
            line_end=entity.line_end,
            severity=entity.severity.value,
            message=entity.message
        )
