# Быстрая справка по анализаторам

## 📦 Установленные анализаторы

### Python (3 анализатора)
| Имя | Расширение | Линтер | Функции |
|-----|-----------|--------|---------|
| `PylintAnalyser` | `.py` | Pylint | Ошибки, стиль, сложность |
| `Flake8Analyser` | `.py` | Flake8 | PEP8 стиль, ошибки |
| `PyrightAnalyser` | `.py` | Pyright | Проверка типов |

**Установка:**
```bash
pip install pylint flake8 pyright
```

---

### JavaScript/TypeScript (3 анализатора)
| Имя | Расширение | Инструмент | Функции |
|-----|-----------|-----------|---------|
| `ESLintAnalyser` | `.js` | ESLint | Синтаксис, лучшие практики |
| `TSLintAnalyser` | `.ts` | TSLint | TypeScript правила |
| `PrettierAnalyser` | `.js` | Prettier | Проверка форматирования |

**Установка:**
```bash
npm install -g eslint tslint prettier
```

---

### Java (1 анализатор)
| Имя | Расширение | Инструмент | Функции |
|-----|-----------|-----------|---------|
| `CheckstyleAnalyser` | `.java` | Checkstyle | Стиль кода, соглашения |

**Установка:**
```bash
# Скачать: https://checkstyle.org/
# Или использовать Maven plugin
```

---

### Go (1 анализатор)
| Имя | Расширение | Инструмент | Функции |
|-----|-----------|-----------|---------|
| `GoLintAnalyser` | `.go` | golangci-lint | Ошибки, стиль, безопасность |

**Установка:**
```bash
https://golangci-lint.run/usage/install/
```

---

### Rust (1 анализатор)
| Имя | Расширение | Инструмент | Функции |
|-----|-----------|-----------|---------|
| `ClippyAnalyser` | `.rs` | Clippy | Ошибки, производительность |

**Установка:**
```bash
rustup component add clippy
```

---

### Универсальные (3 анализатора)
| Имя | Функции |
|-----|---------|
| `RegexPatternAnalyser` | TODO, FIXME, длинные строки |
| `SecurityAnalyser` | Захардкодированные пароли, SQL инъекции, eval() |
| `ComplexityAnalyser` | Вложенность, длинные функции |

---

## 🚀 Быстрый старт

### Анализ одного файла
```python
from infra.analysers import Flake8Analyser

analyser = Flake8Analyser()
analyser.analyse("script.py", lambda issues: 
    print(f"Found {len(issues)} issues"))
```

### Получение анализатора по расширению
```python
from infra.analysers import get_analyser_by_extension

analyser = get_analyser_by_extension(".py")
analyser.analyse("file.py", on_complete)
```

### Получение всех анализаторов
```python
from infra.analysers import get_all_analysers

for analyser in get_all_analysers():
    analyser.analyse(file_path, on_complete)
```

---

## 📊 Матрица поддерживаемых файлов

```
.py  → PylintAnalyser, Flake8Analyser, PyrightAnalyser + Security + Complexity
.js  → ESLintAnalyser, PrettierAnalyser + Security
.ts  → TSLintAnalyser, ESLintAnalyser + Security
.tsx → TSLintAnalyser, ESLintAnalyser + Security
.jsx → ESLintAnalyser + Security
.java → CheckstyleAnalyser + Security
.go  → GoLintAnalyser + Security
.rs  → ClippyAnalyser + Security
OTHER → SecurityAnalyser, RegexPatternAnalyser
```

---

## 🔍 Примеры использования

### Пример 1: Анализ проекта Python
```python
from infra.analysers import PylintAnalyser, Flake8Analyser
from pathlib import Path

def analyse_python_project(project_dir):
    analysers = [PylintAnalyser(), Flake8Analyser()]
    
    for py_file in Path(project_dir).rglob("*.py"):
        for analyser in analysers:
            issues = []
            analyser.analyse(str(py_file), lambda i: issues.extend(i))
            
            print(f"{py_file}: {analyser.name} found {len(issues)} issues")

analyse_python_project("./src")
```

### Пример 2: Проверка безопасности
```python
from infra.analysers import SecurityAnalyser

analyser = SecurityAnalyser()

def print_security_issues(issues):
    critical = [i for i in issues if i.severity.name == "CRIT"]
    if critical:
        print(f"⚠️  {len(critical)} CRITICAL issues found!")
        for issue in critical:
            print(f"  {issue.file_path}:{issue.line_start} - {issue.message}")

analyser.analyse("config.py", print_security_issues)
```

### Пример 3: Интеграция с FastAPI
```python
@app.post("/analyse")
def analyse_file(file_path: str):
    from infra.analysers import get_analyser_by_extension
    
    ext = Path(file_path).suffix
    analyser = get_analyser_by_extension(ext)
    
    issues = []
    analyser.analyse(file_path, lambda i: issues.extend(i))
    
    return {
        "file": file_path,
        "analyser": analyser.name,
        "issues": len(issues),
        "details": [
            {
                "line": issue.line_start,
                "severity": issue.severity.name,
                "message": issue.message
            }
            for issue in issues
        ]
    }
```

---

## ⚙️ Конфигурация

### Включение конкретного анализатора
```python
from app.service_container import ServiceContainer
from infra.analysers import PylintAnalyser, ESLintAnalyser

container = ServiceContainer(
    uow=uow,
    repo_manager=repo_manager,
    auth_client=auth_client,
    analysers=[
        PylintAnalyser(),
        ESLintAnalyser(),
    ]  # Только эти два
)
```

### Исключение анализаторов
```python
from infra.analysers import get_all_analysers

all_analysers = get_all_analysers()
filtered = [a for a in all_analysers if a.ext != ".java"]

container = ServiceContainer(..., analysers=filtered)
```

---

## 🐛 Отладка

### Проверка установки анализаторов
```bash
# Python
python -c "import pylint; print(pylint.__version__)"

# JavaScript
eslint --version

# Go
golangci-lint version

# Rust
cargo clippy --version
```

### Тест анализатора
```python
from infra.analysers import PylintAnalyser

analyser = PylintAnalyser()

# Создаем тестовый файл
test_file = "test_script.py"
with open(test_file, "w") as f:
    f.write("import os\nx = 1  # Неиспользуемая переменная")

# Анализируем
issues = []
analyser.analyse(test_file, lambda i: issues.extend(i))

print(f"Found {len(issues)} issues: {[i.message for i in issues]}")
```

---

## 📚 Дополнительные ресурсы

- `ANALYSERS_GUIDE.md` - Полная документация
- `EXAMPLES.py` - Примеры использования
- `EXTENSION_GUIDE.md` - Как создать свой анализатор
- `base.py` - Исходный код BaseAnalyser

---

## 🎯 Часто используемые команды

```python
# Получить все Issue с ошибками
critical_issues = [i for i in issues if i.severity.name == "CRIT"]

# Сортировка по строке
sorted_issues = sorted(issues, key=lambda i: i.line_start)

# Группировка по файлам
from itertools import groupby
by_file = groupby(sorted(issues, key=lambda i: i.file_path), 
                   lambda i: i.file_path)

# Статистика
stats = {
    "CRIT": sum(1 for i in issues if i.severity.name == "CRIT"),
    "ERR": sum(1 for i in issues if i.severity.name == "ERR"),
    "WARN": sum(1 for i in issues if i.severity.name == "WARN"),
    "INFO": sum(1 for i in issues if i.severity.name == "INFO"),
}
```

---

## ✅ Чек-лист для добавления нового анализатора

- [ ] Создать класс наследующий BaseAnalyser
- [ ] Реализовать _run_linter()
- [ ] Реализовать _parse_output()
- [ ] Добавить в __init__.py
- [ ] Написать unit тесты
- [ ] Добавить в документацию
- [ ] Добавить примеры использования

---

**Разработано для LintSlayer** 🚀
