from typing import Callable, Protocol
from domain.entities import AnalysisRun
from domain.services.analysis_service import AnalysisService
from ..interfaces.uow import IUnitOfWork
from ..interfaces.analyser import IAnalyser


class IStartAnalysisUseCase(Protocol):
    def __call__(self, project_id: int) -> tuple[Callable[[str, str], None], 'AnalysisRun']:
        ...


class StartAnalysisUseCase:
    """Use case для запуска анализа (application layer)"""
    
    def __init__(self,
                 analysers: list[IAnalyser],
                 analysis_service: AnalysisService,
                 uow: IUnitOfWork):
        self.analysers = analysers
        self.analysis_service = analysis_service
        self.uow = uow


    def __call__(self, project_id: int) -> tuple[Callable[[str, str], None], AnalysisRun]:
        """Запускает анализ проекта и возвращает callback для анализа файлов и объект run"""
        with self.uow:
            # Создаем новый run через domain service
            run = self.analysis_service.createRun(project_id)
            self.uow.runs.add(run)
        
        # Создаем closure, который захватывает run
        def analyse_file_handler(ext: str, path: str) -> None:
            # Находим подходящий анализатор
            analyser = self._findAnalyser(ext)
            if not analyser:
                return
            
            # Запускаем анализ с callback'ом, который захватывает run
            def on_analysis_complete(issues):
                self._onAnalysisComplete(run, issues)
            
            analyser.analyse(path, on_analysis_complete)
        
        return analyse_file_handler, run


    def _findAnalyser(self, ext: str) -> IAnalyser | None:
        """Находит подходящий анализатор по расширению"""
        for analyser in self.analysers:
            if hasattr(analyser, 'ext') and ext == analyser.ext:
                return analyser
        return None


    def _onAnalysisComplete(self, run: AnalysisRun, issues) -> None:
        """Callback для сохранения результатов анализа"""
        with self.uow:
            # Устанавливаем run_id для каждого issue
            for issue in issues:
                issue.run_id = run.id
            
            # Сохраняем найденные issues
            self.uow.issues.add_many(issues)
            
            # Обновляем статус run через domain service
            self.analysis_service.completeRun(run)
            
            # Сохраняем изменения в БД
            self.uow.runs.update(run)
