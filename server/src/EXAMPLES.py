"""
Примеры использования новой архитектуры DDD & Clean Architecture
"""

# ============================================================================
# ПРИМЕР 1: Использование в FastAPI контроллере
# ============================================================================

from fastapi import FastAPI, Depends, HTTPException
from app.service_container import ServiceContainer
from app.initialization import get_app_container
from app.services import ProjectService, AnalysisRunService
from app.dtos import RepoFromUrl

app = FastAPI()


# Dependency для FastAPI
def get_project_service() -> ProjectService:
    """Получает ProjectService из контейнера"""
    container = get_app_container()
    return container.get_project_service()


def get_analysis_service() -> AnalysisRunService:
    """Получает AnalysisRunService из контейнера"""
    container = get_app_container()
    return container.get_analysis_run_service()


# Контроллер для создания проекта
@app.post("/api/v1/projects")
def create_project(
    owner_id: int,
    repo_url: str,
    service: ProjectService = Depends(get_project_service),
):
    """
    Создает новый проект.
    
    Поток:
    1. FastAPI вызывает контроллер
    2. FastAPI инжектит ProjectService через Depends
    3. ProjectService.create_project() вызывает CreateProjectUseCase
    4. UseCase обрабатывает создание и сохранение
    5. Возвращаем результат
    """
    try:
        repo = RepoFromUrl(repo_url)
        project = service.create_project(owner_id, repo)
        return {
            "id": project.id,
            "owner_id": project.owner,
            "repo_path": str(project.repo_path),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Контроллер для получения проектов пользователя
@app.get("/api/v1/users/{user_id}/projects")
def get_user_projects(
    user_id: int,
    service: ProjectService = Depends(get_project_service),
):
    """Получает все проекты пользователя"""
    projects = service.get_user_projects(user_id)
    return [
        {
            "id": p.id,
            "owner_id": p.owner,
            "repo_path": str(p.repo_path),
        }
        for p in projects
    ]


# Контроллер для запуска анализа
@app.post("/api/v1/projects/{project_id}/analyses")
def start_analysis(
    project_id: int,
    project_service: ProjectService = Depends(get_project_service),
    analysis_service: AnalysisRunService = Depends(get_analysis_service),
):
    """
    Запускает анализ проекта.
    
    Поток:
    1. Получаем информацию о проекте
    2. Запускаем анализ через StartAnalysisUseCase
    3. Use case создает AnalysisRun через AnalysisService
    4. Анализаторы обрабатывают файлы
    5. Результаты сохраняются
    """
    try:
        project = project_service.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        analysis_service.startAnalysis(project_id, project)
        
        return {
            "status": "Analysis started",
            "project_id": project_id,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# ПРИМЕР 2: Прямое использование сервисов (без FastAPI)
# ============================================================================

def example_direct_usage():
    """Пример прямого использования сервисов"""
    from app.initialization import get_app_container
    from app.dtos import RepoFromUrl, RepoFromPath
    from pathlib import Path
    
    # Получаем контейнер
    container = get_app_container()
    
    # Получаем сервисы
    project_service = container.get_project_service()
    analysis_service = container.get_analysis_run_service()
    
    # Создаем проект из URL
    owner_id = 123
    repo = RepoFromUrl("https://github.com/user/repo.git")
    project = project_service.create_project(owner_id, repo)
    print(f"✅ Created project {project.id}")
    
    # Запускаем анализ
    analysis_service.startAnalysis(project.id, project)
    print(f"✅ Analysis started for project {project.id}")
    
    # Получаем информацию о проекте
    updated_project = project_service.get_project(project.id)
    print(f"✅ Retrieved project: {updated_project}")
    
    # Получаем проекты пользователя
    user_projects = project_service.get_user_projects(owner_id)
    print(f"✅ User {owner_id} has {len(user_projects)} projects")


# ============================================================================
# ПРИМЕР 3: Использование Use Cases напрямую
# ============================================================================

def example_use_case_direct():
    """Пример прямого использования Use Cases"""
    from app.initialization import get_app_container
    from app.dtos import RepoFromPath
    from pathlib import Path
    
    container = get_app_container()
    
    # Использование CreateProjectUseCase напрямую
    repo = RepoFromPath(Path("./my-repo"))
    project = container.create_project_uc.execute(owner=456, repo=repo)
    print(f"✅ Created project via use case: {project.id}")
    
    # Использование StartAnalysisUseCase напрямую
    analyse_callback = container.start_analysis_uc.execute(project.id)
    
    # Анализируем файлы
    with open("./my-repo/script.py") as f:
        content = f.read()
        analyse_callback(".py", content)
    
    print(f"✅ Analysis completed")
    
    # Использование GetUserProjectsUseCase напрямой
    projects = container.get_user_projects_uc.execute(owner_id=456)
    print(f"✅ User has {len(projects)} projects")
    
    # Удаление проекта
    container.delete_project_uc.execute(project.id)
    print(f"✅ Deleted project {project.id}")


# ============================================================================
# ПРИМЕР 4: Testing с использованием Mock объектов
# ============================================================================

from unittest.mock import Mock, MagicMock
from domain.services import AnalysisService
from app.use_cases import CreateProjectUseCase
from domain.entities import Project


def example_testing():
    """Пример юнит-тестирования с Mock объектами"""
    
    # Создаем Mock объекты
    mock_uow = Mock()
    mock_repo_manager = Mock()
    
    # Настраиваем Mock для возврата пути
    from pathlib import Path
    mock_repo_manager.downloadRepo.return_value = Path("/tmp/repo")
    
    # Создаем use case с mock объектами
    uc = CreateProjectUseCase(
        repo_manager=mock_repo_manager,
        uow=mock_uow,
    )
    
    # Используем use case
    from app.dtos import RepoFromUrl
    repo = RepoFromUrl("https://github.com/user/repo.git")
    
    # Вызываем метод
    project = uc.execute(owner=1, repo=repo)
    
    # Проверяем, что методы были вызваны
    assert mock_repo_manager.downloadRepo.called
    assert mock_uow.projects.add.called
    assert mock_uow.commit.called
    
    print("✅ All assertions passed")


# ============================================================================
# ПРИМЕР 5: Domain Service использование
# ============================================================================

def example_domain_service():
    """Пример использования Domain Services"""
    from domain.services import AnalysisService
    from domain.values import Status
    
    # Создаем domain service
    service = AnalysisService()
    
    # Создаем run через service
    run = service.createRun(project_id=1)
    assert run.status == Status.RUNNING
    print(f"✅ Run created with status: {run.status}")
    
    # Завершаем run
    service.completeRun(run, success=True)
    assert run.status == Status.COMPLETED
    print(f"✅ Run completed with status: {run.status}")


# ============================================================================
# ПРИМЕР 6: Интеграционный тест
# ============================================================================

def example_integration_test():
    """Пример интеграционного теста"""
    from app.initialization import get_app_container
    from app.dtos import RepoFromPath
    from pathlib import Path
    import tempfile
    
    # Создаем временную директорию для тестирования
    with tempfile.TemporaryDirectory() as tmpdir:
        # Создаем тестовые файлы
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("print('hello')")
        
        # Получаем контейнер
        container = get_app_container()
        
        # Создаем проект
        repo = RepoFromPath(Path(tmpdir))
        project = container.create_project_uc.execute(
            owner=999,
            repo=repo,
        )
        
        # Запускаем анализ
        container.start_analysis_uc.execute(project_id=project.id)
        
        # Получаем результаты
        analyses = container.analysis_run_service.getProjectAnalyses(
            project_id=project.id
        )
        
        print(f"✅ Integration test passed: {len(analyses)} analyses found")


# ============================================================================
# Вспомогательные функции
# ============================================================================

def print_project_info(project):
    """Выводит информацию о проекте"""
    print(f"""
Project Information:
  ID: {project.id}
  Owner: {project.owner_id}
  Path: {project.repo_path}
""")


def print_analysis_info(analysis_run):
    """Выводит информацию об анализе"""
    print(f"""
Analysis Information:
  ID: {analysis_run.id}
  Project: {analysis_run.project_id}
  Status: {analysis_run.status}
  Timestamp: {analysis_run.timestamp}
""")


if __name__ == "__main__":
    print("=" * 80)
    print("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ DDD & CLEAN ARCHITECTURE")
    print("=" * 80)
    
    print("\n📝 ПРИМЕР 1: FastAPI контроллеры")
    print("  → Смотрите примеры выше (create_project, get_user_projects, start_analysis)")
    
    print("\n🔧 ПРИМЕР 2: Прямое использование сервисов")
    print("  → example_direct_usage()")
    
    print("\n⚙️  ПРИМЕР 3: Использование Use Cases")
    print("  → example_use_case_direct()")
    
    print("\n🧪 ПРИМЕР 4: Testing с Mock объектами")
    print("  → example_testing()")
    
    print("\n📦 ПРИМЕР 5: Domain Service использование")
    print("  → example_domain_service()")
    
    print("\n🔗 ПРИМЕР 6: Интеграционный тест")
    print("  → example_integration_test()")
