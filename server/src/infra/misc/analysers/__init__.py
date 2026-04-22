"""
Анализаторы для различных языков программирования
"""

from .python_analysers import PylintAnalyser, Flake8Analyser, PyrightAnalyser
from .javascript_analysers import ESLintAnalyser, TSLintAnalyser, PrettierAnalyser
from .other_analysers import CheckstyleAnalyser, GoLintAnalyser, ClippyAnalyser
from .generic_analysers import RegexPatternAnalyser, SecurityAnalyser, ComplexityAnalyser

__all__ = [
    # Python
    "PylintAnalyser",
    "Flake8Analyser",
    "PyrightAnalyser",
    
    # JavaScript/TypeScript
    "ESLintAnalyser",
    "TSLintAnalyser",
    "PrettierAnalyser",
    
    # Other languages
    "CheckstyleAnalyser",
    "GoLintAnalyser",
    "ClippyAnalyser",
    
    # Generic
    "RegexPatternAnalyser",
    "SecurityAnalyser",
    "ComplexityAnalyser",
]


def get_all_analysers():
    """Возвращает список всех доступных анализаторов"""
    return [
        PylintAnalyser(),
        Flake8Analyser(),
        PyrightAnalyser(),
        ESLintAnalyser(),
        TSLintAnalyser(),
        PrettierAnalyser(),
        CheckstyleAnalyser(),
        GoLintAnalyser(),
        ClippyAnalyser(),
        SecurityAnalyser(),
        ComplexityAnalyser(),
    ]


def get_analyser_by_extension(extension: str):
    """Получает подходящий анализатор по расширению файла"""
    extension = extension.lower()
    
    analysers = get_all_analysers()
    
    # Приоритет анализаторов
    priority = {
        ".py": [PylintAnalyser, Flake8Analyser, PyrightAnalyser],
        ".js": [ESLintAnalyser, PrettierAnalyser],
        ".ts": [TSLintAnalyser, ESLintAnalyser],
        ".tsx": [TSLintAnalyser, ESLintAnalyser],
        ".jsx": [ESLintAnalyser],
        ".java": [CheckstyleAnalyser],
        ".go": [GoLintAnalyser],
        ".rs": [ClippyAnalyser],
    }
    
    # Возвращаем первый подходящий
    for analyser in analysers:
        if analyser.ext == extension:
            return analyser
    
    # Если точного совпадения нет, используем универсальные
    return SecurityAnalyser()
