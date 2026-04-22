"""
Документация по анализаторам кода

## Доступные анализаторы

### Python
1. **PylintAnalyser** (ext: .py)
   - Линтер: Pylint
   - Возможности: выявление ошибок, стиль кода, сложность
   - Установка: pip install pylint
   - Вывод: JSON
   
2. **Flake8Analyser** (ext: .py)
   - Линтер: Flake8
   - Возможности: ошибки, стиль, сложность
   - Установка: pip install flake8
   - Вывод: JSON
   
3. **PyrightAnalyser** (ext: .py)
   - Линтер: Pyright
   - Возможности: проверка типов, ошибки
   - Установка: pip install pyright
   - Вывод: JSON

### JavaScript/TypeScript
1. **ESLintAnalyser** (ext: .js)
   - Линтер: ESLint
   - Возможности: синтаксис, лучшие практики, стиль
   - Установка: npm install eslint
   - Вывод: JSON

2. **TSLintAnalyser** (ext: .ts)
   - Линтер: TSLint
   - Возможности: лучшие практики TypeScript
   - Установка: npm install tslint typescript
   - Вывод: JSON

3. **PrettierAnalyser** (ext: .js)
   - Форматер: Prettier
   - Возможности: проверка форматирования кода
   - Установка: npm install prettier
   - Проверка: prettier --check

### Java
1. **CheckstyleAnalyser** (ext: .java)
   - Линтер: Checkstyle
   - Возможности: стиль кода, соглашения
   - Установка: Скачать с https://checkstyle.org/
   - Вывод: JSON

### Go
1. **GoLintAnalyser** (ext: .go)
   - Линтер: golangci-lint
   - Возможности: ошибки, стиль, безопасность
   - Установка: https://golangci-lint.run/usage/install/
   - Вывод: JSON

### Rust
1. **ClippyAnalyser** (ext: .rs)
   - Линтер: Clippy
   - Возможности: ошибки, производительность, стиль
   - Установка: rustup component add clippy
   - Вывод: JSON (cargo clippy --message-format=json)

### Универсальные анализаторы

1. **RegexPatternAnalyser** (ext: любой)
   - Назначение: базовый анализ по паттернам
   - Обнаруживает: TODO, FIXME, длинные строки, пробелы в конце
   
2. **SecurityAnalyser** (ext: любой)
   - Назначение: поиск проблем безопасности
   - Обнаруживает:
     * Захардкодированные пароли и API ключи (CRITICAL)
     * SQL инъекции (ERROR)
     * Использование eval() (ERROR)
     * Небезопасные функции pickle (ERROR)
     * Слабые хеш-функции (WARNING)
   
3. **ComplexityAnalyser** (ext: .py)
   - Назначение: анализ сложности кода
   - Обнаруживает:
     * Глубокую вложенность (indent level >= 3)
     * Длинные функции (> 50 строк)

## Использование

### В коде приложения

```python
from infra.analysers import get_all_analysers, get_analyser_by_extension

# Получить все доступные анализаторы
analysers = get_all_analysers()

# Получить анализатор для файла
analyser = get_analyser_by_extension(".py")

# Запустить анализ
def on_complete(issues):
    for issue in issues:
        print(f"{issue.file_path}:{issue.line_start} - {issue.message}")

analyser.analyse("path/to/file.py", on_complete)
```

### В DI контейнере

```python
from infra.analysers import get_all_analysers
from app.service_container import ServiceContainer

container = ServiceContainer(
    uow=uow,
    repo_manager=repo_manager,
    auth_client=auth_client,
    analysers=get_all_analysers(),  # Используем все доступные анализаторы
)
```

## Требования для установки линтеров

### Python
```bash
pip install pylint flake8 pyright
```

### JavaScript
```bash
npm install -g eslint tslint prettier
```

### Java
```bash
# Скачать Checkstyle: https://checkstyle.org/
# Или использовать Maven plugin
```

### Go
```bash
https://golangci-lint.run/usage/install/
```

### Rust
```bash
rustup component add clippy
```

## Расширение функционала

Чтобы добавить новый анализатор:

1. Создайте класс, наследующий BaseAnalyser
2. Реализуйте методы _run_linter() и _parse_output()
3. Добавьте его в __init__.py

Пример:

```python
from .base import BaseAnalyser

class MyCustomAnalyser(BaseAnalyser):
    ext = ".my"
    name = "my-analyser"
    
    def _run_linter(self, file_path: str) -> str:
        # Запустить линтер и вернуть вывод
        command = ["my-linter", file_path]
        return self._run_command(command)
    
    def _parse_output(self, output: str, file_path: str) -> List[Issue]:
        # Распарсить вывод и вернуть список Issue
        issues = []
        for line in output.split('\\n'):
            # Парсинг...
            pass
        return issues
```

## Примечания по безопасности

- SecurityAnalyser выполняет только базовый анализ
- Для критических проектов используйте специализированные инструменты безопасности
- SAST инструменты (SonarQube, Checkmarx) могут обеспечить более глубокий анализ
- Все анализаторы запускаются с таймаутом 30 секунд для предотвращения зависаний

## Обработка ошибок

Если линтер не установлен на систему:
- Анализатор вернет RuntimeError с сообщением "Command not found"
- On_complete callback будет вызван с пустым списком

Все ошибки логируются в stdout для отладки.
"""
