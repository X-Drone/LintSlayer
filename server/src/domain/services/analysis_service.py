from domain.entities import AnalysisRun
from domain.values import Status


class AnalysisService:
    """Domain service для управления анализом (бизнес-логика)"""
    
    def createRun(self, project_id: int) -> AnalysisRun:
        """Создает и инициализирует новый run анализа"""
        run = AnalysisRun.create(project_id)
        run.run()  # Переводим в статус RUNNING
        return run
    
    
    def completeRun(self, run: AnalysisRun, success: bool = True) -> None:
        """Завершает run анализа"""
        status = Status.COMPLETED if success else Status.FAILED
        run.complete(status)
