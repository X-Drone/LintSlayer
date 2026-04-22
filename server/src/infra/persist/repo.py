from .mapper import ProjectMapper, AnalysisRunMapper, IssueMapper
from app.interfaces.repo import IProjectRepo, IAnalysisRunRepo, IIssueRepo
from domain.entities import Project, AnalysisRun, Issue
from .models import Project as ProjectModel
from .models import AnalysisRun as AnalysisRunModel
from .models import Issue as IssueModel
from sqlalchemy.orm import Session


class ProjectRepo(IProjectRepo):
    def __init__(self, session: Session):
        self.session: Session = session
    
    def add(self, project: Project):
        model = ProjectMapper.to_model(project)
        self.session.add(model)
        self.session.flush()
        project.id = model.id
    
    def getById(self, id: int) -> Project:
        model = self.session.get(ProjectModel, id)
        if not model:
            raise ValueError(f"Project {id} not found")
        
        domain = ProjectMapper.to_domain(model)
        return domain
    
    def getUserProjects(self, user: str) -> list[Project]:
        models = (
            self.session.query(ProjectModel)
            .filter(ProjectModel.owner == user)
            .all()
        )

        return [
            ProjectMapper.to_domain(model)
                for model in models
        ]
    
    def delete(self, id: int):
        model = self.session.get(ProjectModel, id)
        if model:
            self.session.delete(model)


class AnalysisRunRepo(IAnalysisRunRepo):
    def __init__(self, session: Session):
        self.session = session

    def add(self, run: AnalysisRun):
        model = AnalysisRunMapper.to_model(run)
        self.session.add(model)
        self.session.flush()
        run.id = model.id

    def getById(self, id: int) -> AnalysisRun:
        model = self.session.get(AnalysisRunModel, id)
        if not model:
            raise ValueError(f"AnalysisRun {id} not found")

        return AnalysisRunMapper.to_domain(model)

    def update(self, run: AnalysisRun):
        model = self.session.get(AnalysisRunModel, run.id)
        if not model:
            raise ValueError(f"AnalysisRun {run.id} not found")

        model.status = run.status.value
        model.timestamp = run.timestamp

        self.session.merge(model)

    def getProjectRuns(self, project_id: int) -> list[AnalysisRun]:
        models = (
            self.session.query(AnalysisRunModel)
            .filter(AnalysisRunModel.project_id == project_id)
            .order_by(AnalysisRunModel.id.desc())
            .all()
        )

        return [AnalysisRunMapper.to_domain(m) for m in models]


class IssueRepo(IIssueRepo):
    def __init__(self, session: Session):
        self.session = session

    def add(self, issue: Issue):
        model = IssueMapper.to_model(issue)
        self.session.add(model)
        self.session.flush()
        issue.id = model.id
    
    def add_many(self, issues: list[Issue]):
        models = [IssueMapper.to_model(i) for i in issues]
        self.session.add_all(models)

    def getById(self, id: int) -> Issue:
        model = self.session.get(IssueModel, id)
        if not model:
            raise ValueError(f"Issue {id} not found")

        return IssueMapper.to_domain(model)

    def getAnalysisRunIssues(self, run_id: int) -> list[Issue]:
        models = (
            self.session.query(IssueModel)
            .filter(IssueModel.run_id == run_id)
            # .order_by(IssueModel.severity.desc())
            .all()
        )

        return [IssueMapper.to_domain(m) for m in models]
