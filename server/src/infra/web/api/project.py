from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel as Schema

from domain.entities import *
from domain.services import ProjectService
from domain.values import Severity
from core import settings
from ...misc import container
from app.dtos import RepoFromUrl, RepoFromPath, RepoFromText
from pathlib import Path

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.auth_url+"login")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    user = container.verify_user_token_uc()(token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


router = APIRouter()


class ProjectsResponse(Schema):
    names: list[str]


@router.get("/", response_model=ProjectsResponse)
def get_projects(user: Annotated[str, Depends(get_current_user)]):
    projects: list[Project] = container.get_project_service().get_user_projects(user)
    return ProjectsResponse(
        names=[project.name for project in projects]
    )


class ProjectCreateRequest(Schema):
    name: str
    repo_url: str | None = None
    ext: str | None = None
    content: str | None = None


class ProjectResponse(Schema):
    id: int
    name: str
    owner: str
    files: list[str]


@router.post("/create", response_model=ProjectResponse)
def create_project(user: Annotated[str, Depends(get_current_user)], req: ProjectCreateRequest = Body(...)):
    # Determine repo source based on provided data
    if req.repo_url:
        repo = RepoFromUrl(req.repo_url)
    elif req.content and req.ext:
        repo = RepoFromText(req.content, req.ext)
    else:
        raise HTTPException(status_code=400, detail="Either repo_url or (content + ext) must be provided")
    
    try:
        project = container.get_project_service().create_project(user, req.name, repo)
        base_dir = container.repo_manager.getBaseTempDir()
        files = [str(file).replace(str(base_dir / user), '').lstrip('/\\') for file in container.project_domain_service.getProjectFiles(project)]
        return ProjectResponse(
            id=project.id,
            name=project.name,
            owner=project.owner,
            files=files
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class ProjectDetailResponse(Schema):
    id: int
    name: str
    owner: str
    files: list[str]


@router.get("/{project_id}", response_model=ProjectDetailResponse)
def get_project(project_id: int, user: Annotated[str, Depends(get_current_user)]):
    project = container.get_project_service().get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner != user:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    base_dir = container.repo_manager.getBaseTempDir()
    files = [str(file).replace(str(base_dir / user), '').lstrip('/\\') for file in container.project_domain_service.getProjectFiles(project)]
    return ProjectDetailResponse(
        id=project.id,
        name=project.name,
        owner=project.owner,
        files=files
    )


class AnalysisRunResponse(Schema):
    id: int
    project_id: int
    status: str
    timestamp: str | None


@router.post("/{project_id}/analyse")
def run_analyse(project_id: int, analysers: list[str], user: Annotated[str, Depends(get_current_user)]):
    project = container.get_project_service().get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner != user:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    try:
        run = container.get_analysis_run_service().startAnalysis(project_id, project, [analyser.lower() for analyser in analysers])
        return AnalysisRunResponse(
            id=run.id,
            project_id=run.project_id,
            status=run.status.name,
            timestamp=run.timestamp.isoformat() if run.timestamp else None
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{project_id}/analyses", response_model=list[AnalysisRunResponse])
def get_analyses(project_id: int, user: Annotated[str, Depends(get_current_user)]):
    project = container.get_project_service().get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner != user:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    runs = container.get_analysis_run_service().getProjectAnalyses(project_id)
    return [
        AnalysisRunResponse(
            id=run.id,
            project_id=run.project_id,
            status=run.status.name,
            timestamp=run.timestamp.isoformat() if run.timestamp else None
        )
        for run in runs
    ]


class IssueResponse(Schema):
    id: int
    file_path: str
    line_start: int
    line_end: int
    severity: str
    message: str


class AnalysisDetailResponse(Schema):
    id: int
    project_id: int
    status: str
    timestamp: str | None
    issues: list[IssueResponse]


@router.get("/{project_id}/analyses/{run_id}", response_model=AnalysisDetailResponse)
def get_analyse(project_id: int, run_id: int, user: Annotated[str, Depends(get_current_user)]):
    project = container.get_project_service().get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner != user:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    run = container.get_analysis_run_service().getAnalysisRun(run_id)
    if not run or run.project_id != project_id:
        raise HTTPException(status_code=404, detail="Analysis run not found")
    
    # Get issues for this run
    issues = container.get_analysis_run_issues_uc()(run_id)
    
    base_dir = container.repo_manager.getBaseTempDir()
    return AnalysisDetailResponse(
        id=run.id,
        project_id=run.project_id,
        status=run.status.name,
        timestamp=run.timestamp.isoformat() if run.timestamp else None,
        issues=[
            IssueResponse(
                id=issue.id,
                file_path=str(issue.file_path).replace(str(base_dir / user), '').lstrip('/\\'),
                line_start=issue.line_start,
                line_end=issue.line_end,
                severity=issue.severity.name,
                message=issue.message
            )
            for issue in issues
        ]
    )


@router.delete("/{project_id}")
def delete_project(project_id: int, user: Annotated[str, Depends(get_current_user)]):
    project = container.get_project_service().get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner != user:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    try:
        container.get_project_service().delete_project(project_id)
        return {"status": "Project deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
