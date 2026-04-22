"""
Container для инициализации всех компонентов приложения (DI контейнер).
Централизованное место для создания экземпляров всех сервисов с их зависимостями.
"""

from typing import Protocol
from domain.services import AnalysisService, ProjectService as ProjectDomainService
from app.use_cases import (
    CreateProjectUseCase,
    StartAnalysisUseCase,
    GetUserProjectsUseCase,
    DeleteProjectUseCase,
    GetProjectUseCase,
    VerifyUserTokenUseCase,
)
from app.services import (
    ProjectService,
    AnalysisRunService,
    VerifyUserService,
)
from app.interfaces.uow import IUnitOfWork
from app.interfaces.repo_manager import IRepoManager
from app.interfaces.auth_client import IAuthClient
from app.interfaces.analyser import IAnalyser


class IServiceContainer(Protocol):
    """Интерфейс для DI контейнера"""
    
    # Application Services
    project_service: ProjectService
    analysis_run_service: AnalysisRunService
    verify_user_service: VerifyUserService
    
    # Use Cases
    create_project_uc: CreateProjectUseCase
    start_analysis_uc: StartAnalysisUseCase
    get_user_projects_uc: GetUserProjectsUseCase
    delete_project_uc: DeleteProjectUseCase
    get_project_uc: GetProjectUseCase
    verify_user_token_uc: VerifyUserTokenUseCase


class ServiceContainer:
    """DI контейнер для регистрации и инициализации всех сервисов"""
    
    def __init__(self,
                 uow: IUnitOfWork,
                 repo_manager: IRepoManager,
                 auth_client: IAuthClient,
                 analysers: list[IAnalyser]):
        self.uow = uow
        self.repo_manager = repo_manager
        self.auth_client = auth_client
        self.analysers = analysers
        
        # Инициализируем все компоненты
        self._initialize()
    
    def _initialize(self) -> None:
        """Инициализирует все сервисы и их зависимости"""
        
        # Domain Services
        self.analysis_domain_service = AnalysisService()
        self.project_domain_service = ProjectDomainService()
        
        # Use Cases
        self.create_project_uc = CreateProjectUseCase(
            repo_manager=self.repo_manager,
            uow=self.uow
        )
        
        self.start_analysis_uc = StartAnalysisUseCase(
            analysers=self.analysers,
            analysis_service=self.analysis_domain_service,
            uow=self.uow
        )
        
        self.get_user_projects_uc = GetUserProjectsUseCase(
            uow=self.uow
        )
        
        self.delete_project_uc = DeleteProjectUseCase(
            repo_manager=self.repo_manager,
            uow=self.uow
        )
        
        self.get_project_uc = GetProjectUseCase(
            uow=self.uow
        )
        
        self.verify_user_token_uc = VerifyUserTokenUseCase(
            auth_client=self.auth_client
        )
        
        # Application Services (Координаторы)
        self.project_service = ProjectService(
            create_project_uc=self.create_project_uc,
            delete_project_uc=self.delete_project_uc,
            domain_service=self.project_domain_service,
            uow=self.uow
        )
        
        self.analysis_run_service = AnalysisRunService(
            start_analysis_uc=self.start_analysis_uc,
            domain_service=self.analysis_domain_service,
            uow=self.uow
        )
        
        self.verify_user_service = VerifyUserService(
            auth_client=self.auth_client,
            uow=self.uow
        )
    
    # Expose API для удобного доступа
    def get_project_service(self) -> ProjectService:
        return self.project_service
    
    def get_analysis_run_service(self) -> AnalysisRunService:
        return self.analysis_run_service
    
    def get_verify_user_service(self) -> VerifyUserService:
        return self.verify_user_service


# Пример использования:
# =====================
# 
# # В main.py или в точке входа приложения:
# container = ServiceContainer(
#     uow=PostgresUnitOfWork(),
#     repo_manager=GitRepoManager(),
#     auth_client=ExternalAuthClient(),
#     analysers=[PythonAnalyser(), JavaScriptAnalyser()]
# )
# 
# # Использование в контроллерах/эндпоинтах:
# @app.post("/projects")
# def create_project(owner_id: int, repo: RepoSource):
#     project = container.project_service.create_project(owner_id, repo)
#     return project
# 
# @app.post("/analyses/{project_id}")
# def start_analysis(project_id: int):
#     project = container.project_service.get_project(project_id)
#     container.analysis_run_service.start_analysis(project_id, project)
#     return {"status": "analysis started"}
# 
# @app.get("/users/{user_id}/projects")
# def get_user_projects(user_id: int, token: str):
#     if not container.verify_user_service.verify_token(token):
#         return {"error": "Unauthorized"}
#     
#     projects = container.project_service.get_user_projects(user_id)
#     return projects
