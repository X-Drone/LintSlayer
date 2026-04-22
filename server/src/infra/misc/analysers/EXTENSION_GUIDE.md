# Структура и расширение анализаторов

## Структура папки infra/analysers

```
infra/analysers/
├── __init__.py                    # Экспорт и функции получения анализаторов
├── base.py                        # Базовый класс BaseAnalyser
├── python_analysers.py            # PylintAnalyser, Flake8Analyser, PyrightAnalyser
├── javascript_analysers.py        # ESLintAnalyser, TSLintAnalyser, PrettierAnalyser
├── other_analysers.py             # CheckstyleAnalyser, GoLintAnalyser, ClippyAnalyser
├── generic_analysers.py           # RegexPatternAnalyser, SecurityAnalyser, ComplexityAnalyser
├── ANALYSERS_GUIDE.md             # Документация по использованию
├── EXAMPLES.py                    # Примеры использования
└── EXTENSION_GUIDE.md             # Этот файл
```

## Базовый класс BaseAnalyser

Все анализаторы наследуют от `BaseAnalyser`:

```python
class BaseAnalyser(ABC):
    ext: str              # Расширение файла (.py, .js, .java и т.д.)
    name: str             # Имя анализатора (для логирования)
    
    @abstractmethod
    def _run_linter(self, file_path: str) -> str:
        """Запускает линтер и возвращает вывод"""
        pass
    
    @abstractmethod
    def _parse_output(self, output: str, file_path: str) -> List[Issue]:
        """Парсит вывод линтера в список Issue"""
        pass
```

## Как добавить новый анализатор

### Шаг 1: Создать класс анализатора

```python
from .base import BaseAnalyser
from domain.entities import Issue
from domain.values import Severity

class MyNewAnalyser(BaseAnalyser):
    ext = ".ext"
    name = "my-analyser"
    
    def _run_linter(self, file_path: str) -> str:
        """Запускает линтер и возвращает результат"""
        command = [
            "my-linter",
            "--output=json",
            file_path,
        ]
        return self._run_command(command)  # Метод из BaseAnalyser
    
    def _parse_output(self, output: str, file_path: str) -> List[Issue]:
        """Парсит вывод в Issue объекты"""
        issues = []
        
        try:
            data = json.loads(output)
            
            for item in data:
                severity = self._map_severity(item.get("level", "warning"))
                
                issue = Issue(
                    id=None,
                    run_id=None,
                    file_path=file_path,
                    line_start=item.get("line", 0),
                    line_end=item.get("line", 0),
                    severity=severity,
                    message=item.get("message", ""),
                )
                issues.append(issue)
        
        except Exception as e:
            print(f"Error parsing output: {e}")
        
        return issues
```

### Шаг 2: Добавить в __init__.py

```python
from .my_analyser import MyNewAnalyser

__all__ = [
    # ... existing
    "MyNewAnalyser",
]
```

### Шаг 3: Использовать

```python
from infra.analysers import MyNewAnalyser

analyser = MyNewAnalyser()
def on_complete(issues):
    print(f"Found {len(issues)} issues")

analyser.analyse("file.ext", on_complete)
```

## Полные примеры

### Пример 1: Анализатор с JSON выводом

```python
import json
from .base import BaseAnalyser

class JSONLintAnalyser(BaseAnalyser):
    ext = ".json"
    name = "json-linter"
    
    def _run_linter(self, file_path: str) -> str:
        command = ["jsonlint", "--compact", file_path]
        return self._run_command(command)
    
    def _parse_output(self, output: str, file_path: str) -> List[Issue]:
        issues = []
        
        try:
            lines = output.strip().split('\n')
            for line in lines:
                data = json.loads(line)
                issue = Issue(
                    id=None,
                    run_id=None,
                    file_path=file_path,
                    line_start=data.get("line", 0),
                    line_end=data.get("line", 0),
                    severity=Severity.ERR,
                    message=data.get("error", "JSON parsing error"),
                )
                issues.append(issue)
        except json.JSONDecodeError:
            print("Failed to parse JSON linter output")
        
        return issues
```

### Пример 2: Анализатор с текстовым выводом

```python
import re
from .base import BaseAnalyser

class SimpleLintAnalyser(BaseAnalyser):
    ext = ".simple"
    name = "simple-linter"
    
    def _run_linter(self, file_path: str) -> str:
        command = ["simple-lint", file_path]
        return self._run_command(command)
    
    def _parse_output(self, output: str, file_path: str) -> List[Issue]:
        issues = []
        
        # Парсим текстовый формат: file.ext:10:ERROR:message
        pattern = r"(.+?):(\d+):(\w+):(.+)"
        
        for match in re.finditer(pattern, output):
            line_num = int(match.group(2))
            severity_str = match.group(3)
            message = match.group(4)
            
            severity = self._map_severity(severity_str)
            
            issue = Issue(
                id=None,
                run_id=None,
                file_path=file_path,
                line_start=line_num,
                line_end=line_num,
                severity=severity,
                message=message,
            )
            issues.append(issue)
        
        return issues
```

### Пример 3: Анализатор на основе регулярных выражений

```python
import re
from .base import BaseAnalyser

class RegexAnalyser(BaseAnalyser):
    ext = ".ts"
    name = "regex-analyser"
    
    PATTERNS = {
        "var_keyword": (
            r"\bvar\s+\w+",
            Severity.WARN,
            "Use 'let' or 'const' instead of 'var'"
        ),
        "console_log": (
            r"console\.(log|debug|warn)",
            Severity.INFO,
            "Remove console logs from production code"
        ),
    }
    
    def _run_linter(self, file_path: str) -> str:
        with open(file_path, 'r') as f:
            return f.read()
    
    def _parse_output(self, content: str, file_path: str) -> List[Issue]:
        issues = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for pattern_name, (pattern, severity, message) in self.PATTERNS.items():
                if re.search(pattern, line):
                    issue = Issue(
                        id=None,
                        run_id=None,
                        file_path=file_path,
                        line_start=line_num,
                        line_end=line_num,
                        severity=severity,
                        message=message,
                    )
                    issues.append(issue)
        
        return issues
```

### Пример 4: Асинхронный анализатор

```python
import asyncio
from typing import List
from .base import BaseAnalyser

class AsyncAnalyser(BaseAnalyser):
    ext = ".async"
    name = "async-analyser"
    
    def _run_linter(self, file_path: str) -> str:
        # Запускаем асинхронный процесс синхронно
        return asyncio.run(self._async_lint(file_path))
    
    async def _async_lint(self, file_path: str) -> str:
        """Асинхронный анализ"""
        # Можно использовать asyncio для параллельного анализа
        # и других асинхронных операций
        command = ["async-linter", file_path]
        return self._run_command(command)
    
    def _parse_output(self, output: str, file_path: str) -> List[Issue]:
        # Парсинг вывода
        pass
```

## Тестирование нового анализатора

```python
import pytest
from infra.analysers import MyNewAnalyser
from domain.values import Severity

def test_my_new_analyser():
    analyser = MyNewAnalyser()
    
    issues = []
    def on_complete(found_issues):
        issues.extend(found_issues)
    
    analyser.analyse("test_file.ext", on_complete)
    
    assert len(issues) > 0
    assert issues[0].severity in [Severity.INFO, Severity.WARN, Severity.ERR, Severity.CRIT]
    
def test_my_analyser_error_handling():
    analyser = MyNewAnalyser()
    
    issues = []
    def on_complete(found_issues):
        issues.extend(found_issues)
    
    # Анализируем несуществующий файл
    analyser.analyse("nonexistent.ext", on_complete)
    
    # Should handle gracefully
    assert isinstance(issues, list)
```

## Лучшие практики

### 1. Обработка ошибок
- Всегда оборачивайте парсинг в try-except
- Логируйте ошибки для отладки
- Возвращайте пустой список если ошибка

### 2. Производительность
- Таймаут 30 секунд встроен в _run_command
- Для больших файлов может потребоваться оптимизация
- Кешируйте результаты если возможно

### 3. Поддержка различных версий
- Тестируйте с разными версиями линтеров
- Обработка изменений в формате вывода
- Документируйте требуемые версии

### 4. Расширяемость
- Используйте protected методы (_run_command, _map_severity)
- Наследуйте от BaseAnalyser для общей логики
- Переопределяйте только необходимое

## Интеграция с дополнительными инструментами

### Pre-commit hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: custom-analyser
        name: Custom Lint
        entry: python -m infra.analysers.EXAMPLES
        language: python
        types: [python]
```

### CI/CD интеграция
```yaml
# .github/workflows/lint.yml
name: Lint
on: [push]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: python analyse_project.py
```

## Устранение проблем

### Анализатор не найден
```
❌ Error: Command not found: my-linter
💡 Установите анализатор: pip install my-linter
```

### Неправильный формат вывода
```
❌ Failed to parse output as JSON
💡 Проверьте параметры команды, используйте --output-format
```

### Таймаут
```
❌ Command timed out
💡 Анализатор занял > 30 секунд, оптимизируйте
```

## Документирование анализатора

```python
class DocumentedAnalyser(BaseAnalyser):
    """
    Анализатор для MyLang используя MyLint
    
    Requires:
        - MyLint >= 1.0 (pip install my-lint)
    
    Features:
        - Syntax checking
        - Style validation
        - Performance analysis
    
    Output format:
        JSON with keys: line, severity, message
    
    Example:
        analyser = DocumentedAnalyser()
        analyser.analyse("file.ml", on_complete)
    """
    ext = ".ml"
    name = "mylint"
    # ...
```

---

Для добавления новых анализаторов следуйте этим шагам и лучшим практикам!
