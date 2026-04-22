from pathlib import Path
from domain.entities import Project


class ProjectService:
    """Domain service для управления проектами (бизнес-логика)"""
    
    def validateRepoPath(self, path: Path) -> bool:
        """Валидирует путь репозитория"""
        return path.exists() and path.is_dir()
    

    def getProjectFiles(self, project: Project) -> list[Path]:
        """Получает все файлы в проекте"""
        return [f for f in project.repo_path.rglob('*') if f.is_file()]
