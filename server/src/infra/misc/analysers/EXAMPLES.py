"""
Примеры использования анализаторов кода
"""

from server.src.infra.misc.analysers import (
    PylintAnalyser,
    Flake8Analyser,
    ESLintAnalyser,
    SecurityAnalyser,
    get_all_analysers,
    get_analyser_by_extension,
)


# ============================================================================
# ПРИМЕР 1: Использование отдельного анализатора
# ============================================================================

def example_single_analyser():
    """Пример анализа одного файла одним анализатором"""
    
    analyser = PylintAnalyser()
    
    def on_analysis_complete(issues):
        print(f"Found {len(issues)} issues:\n")
        for issue in issues:
            print(f"  {issue.file_path}:{issue.line_start}")
            print(f"    {issue.severity.name}: {issue.message}\n")
    
    # Анализируем файл
    analyser.analyse("path/to/script.py", on_analysis_complete)


# ============================================================================
# ПРИМЕР 2: Использование всех анализаторов для файла
# ============================================================================

def example_all_analysers():
    """Пример запуска всех подходящих анализаторов для файла"""
    
    file_path = "path/to/script.py"
    extension = ".py"
    
    analysers = get_all_analysers()
    
    # Фильтруем анализаторы для нужного расширения
    matching_analysers = [a for a in analysers if a.ext == extension]
    
    all_issues = []
    
    def on_complete(issues):
        all_issues.extend(issues)
    
    # Запускаем все подходящие анализаторы
    for analyser in matching_analysers:
        print(f"Running {analyser.name}...")
        analyser.analyse(file_path, on_complete)
    
    print(f"\nTotal issues found: {len(all_issues)}")
    
    # Группируем по серьезности
    by_severity = {}
    for issue in all_issues:
        severity = issue.severity.name
        if severity not in by_severity:
            by_severity[severity] = []
        by_severity[severity].append(issue)
    
    print("\nIssues by severity:")
    for severity, issues_list in sorted(by_severity.items()):
        print(f"  {severity}: {len(issues_list)}")


# ============================================================================
# ПРИМЕР 3: Выбор анализатора по расширению
# ============================================================================

def example_get_by_extension():
    """Пример получения подходящего анализатора по расширению"""
    
    files = [
        "myapp.py",
        "app.js",
        "types.ts",
        "Main.java",
        "main.go",
        "lib.rs",
    ]
    
    for file_path in files:
        extension = "." + file_path.split(".")[-1]
        analyser = get_analyser_by_extension(extension)
        
        print(f"{file_path} → {analyser.name}")


# ============================================================================
# ПРИМЕР 4: Анализ проекта на проблемы безопасности
# ============================================================================

def example_security_analysis():
    """Пример анализа файлов на проблемы безопасности"""
    
    security_analyser = SecurityAnalyser()
    
    files = [
        "config.py",
        "auth.js",
        "database.py",
    ]
    
    critical_issues = []
    
    def on_complete(issues):
        # Фильтруем критические проблемы
        critical = [i for i in issues if i.severity.name == "ERR" or i.severity.name == "CRIT"]
        critical_issues.extend(critical)
    
    for file_path in files:
        print(f"Scanning {file_path}...")
        security_analyser.analyse(file_path, on_complete)
    
    if critical_issues:
        print(f"\n⚠️  CRITICAL SECURITY ISSUES FOUND: {len(critical_issues)}\n")
        for issue in critical_issues:
            print(f"  {issue.message}")
            print(f"    File: {issue.file_path}:{issue.line_start}\n")
    else:
        print("\n✅ No critical security issues found")


# ============================================================================
# ПРИМЕР 5: Интеграция с DI контейнером
# ============================================================================

def example_with_di_container():
    """Пример использования анализаторов через DI контейнер"""
    
    from app.initialization import get_app_container
    
    # Получаем контейнер с инициализированными анализаторами
    container = get_app_container()
    
    # Использование в StartAnalysisUseCase
    project_id = 1
    analyse_callback = container.start_analysis_uc.execute(project_id)
    
    # Анализируем файл
    with open("myfile.py") as f:
        content = f.read()
    
    # Callback обработает анализ через все доступные анализаторы
    analyse_callback(".py", content)
    
    print("✅ Analysis completed")


# ============================================================================
# ПРИМЕР 6: Обработка ошибок при анализе
# ============================================================================

def example_error_handling():
    """Пример обработки ошибок при анализе"""
    
    analyser = PylintAnalyser()
    
    def on_complete(issues):
        if not issues:
            print("⚠️  No issues found (or analyser not installed)")
        else:
            print(f"✅ Found {len(issues)} issues")
    
    try:
        analyser.analyse("nonexistent.py", on_complete)
    except FileNotFoundError:
        print("❌ File not found")
    except RuntimeError as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure pylint is installed: pip install pylint")


# ============================================================================
# ПРИМЕР 7: Асинхронный анализ нескольких файлов
# ============================================================================

def example_batch_analysis():
    """Пример анализа нескольких файлов"""
    
    import os
    from pathlib import Path
    
    project_dir = Path("./src")
    python_files = list(project_dir.rglob("*.py"))[:5]  # Первые 5 файлов
    
    analyser = Flake8Analyser()
    all_issues = []
    
    def on_complete(issues):
        all_issues.extend(issues)
    
    print(f"Analyzing {len(python_files)} Python files...\n")
    
    for file_path in python_files:
        try:
            print(f"  {file_path.name}...", end=" ")
            analyser.analyse(str(file_path), on_complete)
            print("✓")
        except Exception as e:
            print(f"✗ ({e})")
    
    # Статистика
    print(f"\n{'='*50}")
    print(f"Total issues found: {len(all_issues)}")
    
    by_severity = {}
    for issue in all_issues:
        severity = issue.severity.name
        if severity not in by_severity:
            by_severity[severity] = 0
        by_severity[severity] += 1
    
    print("\nBreakdown:")
    for severity, count in sorted(by_severity.items(), reverse=True):
        print(f"  {severity:8} {count:3} issues")


# ============================================================================
# ПРИМЕР 8: Кастомный анализатор
# ============================================================================

from server.src.infra.misc.analysers.base import BaseAnalyser
from domain.entities import Issue
from domain.values import Severity


class CustomLinterAnalyser(BaseAnalyser):
    """Кастомный анализатор на основе регулярных выражений"""
    
    ext = ".py"
    name = "custom-linter"
    
    def _run_linter(self, file_path: str) -> str:
        """Читает файл напрямую"""
        with open(file_path, 'r') as f:
            return f.read()
    
    def _parse_output(self, content: str, file_path: str) -> list[Issue]:
        """Ищет кастомные нарушения"""
        import re
        
        issues = []
        lines = content.split('\n')
        
        # Проверяем на использование print вместо logger
        for line_num, line in enumerate(lines, 1):
            if re.search(r'\bprint\s*\(', line):
                issue = Issue(
                    id=None,
                    run_id=None,
                    file_path=file_path,
                    line_start=line_num,
                    line_end=line_num,
                    severity=Severity.WARN,
                    message="Use logger instead of print()",
                )
                issues.append(issue)
        
        return issues


def example_custom_analyser():
    """Пример использования кастомного анализатора"""
    
    analyser = CustomLinterAnalyser()
    
    def on_complete(issues):
        for issue in issues:
            print(f"{issue.file_path}:{issue.line_start} - {issue.message}")
    
    analyser.analyse("myapp.py", on_complete)


# ============================================================================
# Вспомогательные функции
# ============================================================================

def print_issue_summary(issues):
    """Выводит сводку по проблемам"""
    print(f"\n{'='*60}")
    print(f"Total Issues: {len(issues)}")
    print(f"{'='*60}\n")
    
    # Группировка по файлам
    by_file = {}
    for issue in issues:
        if issue.file_path not in by_file:
            by_file[issue.file_path] = []
        by_file[issue.file_path].append(issue)
    
    for file_path, file_issues in sorted(by_file.items()):
        print(f"📄 {file_path}")
        for issue in file_issues:
            severity_emoji = {
                "INFO": "ℹ️ ",
                "WARN": "⚠️ ",
                "ERR": "❌",
                "CRIT": "🔴",
            }
            emoji = severity_emoji.get(issue.severity.name, "❓")
            print(f"  {emoji} Line {issue.line_start}: {issue.message}")
        print()


def filter_issues_by_severity(issues, min_severity):
    """Фильтрует проблемы по минимальной серьезности"""
    severity_levels = {"INFO": 0, "WARN": 1, "ERR": 2, "CRIT": 3}
    min_level = severity_levels.get(min_severity, 0)
    
    return [
        i for i in issues
        if severity_levels.get(i.severity.name, 0) >= min_level
    ]


if __name__ == "__main__":
    print("="*60)
    print("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ АНАЛИЗАТОРОВ КОДА")
    print("="*60)
    
    print("\n1️⃣  example_single_analyser()")
    print("   → Анализ одного файла одним анализатором\n")
    
    print("2️⃣  example_all_analysers()")
    print("   → Запуск всех подходящих анализаторов\n")
    
    print("3️⃣  example_get_by_extension()")
    print("   → Получение анализатора по расширению\n")
    
    print("4️⃣  example_security_analysis()")
    print("   → Анализ на проблемы безопасности\n")
    
    print("5️⃣  example_with_di_container()")
    print("   → Использование с DI контейнером\n")
    
    print("6️⃣  example_error_handling()")
    print("   → Обработка ошибок\n")
    
    print("7️⃣  example_batch_analysis()")
    print("   → Анализ нескольких файлов\n")
    
    print("8️⃣  example_custom_analyser()")
    print("   → Кастомный анализатор\n")
