from typing import Callable
from pathlib import Path
from domain.entities import AnalysisRun, Project
from domain.services.analysis_service import AnalysisService as AnalysisDomainService
from ..interfaces.analyser import IAnalyser
from ..interfaces.uow import IUnitOfWork
from ..use_cases.start_analysis import StartAnalysisUseCase


class AnalysisRunService:
    """Application service для управления анализами (Clean Architecture)"""
    
    def __init__(self,
                 start_analysis_uc: StartAnalysisUseCase,
                 domain_service: AnalysisDomainService,
                 uow: IUnitOfWork):
        self.start_analysis_uc = start_analysis_uc
        self.domain_service = domain_service
        self.uow = uow


    def startAnalysis(self, project_id: int, project: Project) -> AnalysisRun:
        """Запускает анализ проекта"""
        analyse_callback, run = self.start_analysis_uc(project_id)
        
        # Проходим по всем файлам проекта
        for file_path in project.repo_path.rglob('*'):
            if file_path.is_file():
                # Линтеры скорее всего не поддержат чтение файла напрмую
                # with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                #     try:
                #         content = f.read()
                #         analyse_callback(file_path.suffix, content)
                #     except Exception as e:
                #         print(f"Error reading file {file_path}: {e}")
                # Поэтому засунем туда путь
                analyse_callback(file_path.suffix, str(file_path))
        
        return run


    def getAnalysisRun(self, run_id: int) -> AnalysisRun | None:
        """Получает информацию об анализе"""
        with self.uow:
            return self.uow.runs.getById(run_id)


    def getProjectAnalyses(self, project_id: int) -> list[AnalysisRun]:
        """Получает все анализы проекта"""
        with self.uow:
            return self.uow.runs.getProjectRuns(project_id)
