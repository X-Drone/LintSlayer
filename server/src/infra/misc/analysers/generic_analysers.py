"""
Универсальный анализатор на основе регулярных выражений для базового анализа
"""

import re
from typing import List
from domain.entities import Issue
from domain.values import Severity
from .base import BaseAnalyser


class RegexPatternAnalyser(BaseAnalyser):
    """Базовый анализатор на основе паттернов для простого анализа кода"""
    
    ext = "any"
    name = "Regex Patterns"
    
    # Паттерны для обнаружения проблем
    PATTERNS = {
        "todo": (r"#\s*TODO\s*:?", Severity.INFO, "TODO comment found"),
        "fixme": (r"#\s*FIXME\s*:?|@FIXME", Severity.WARN, "FIXME comment found"),
        "trailing_whitespace": (r"\s+$", Severity.INFO, "Trailing whitespace"),
        "long_line": (r".{120,}", Severity.WARN, "Line too long (>120 chars)"),
    }
    
    def _run_linter(self, file_path: str) -> str:
        """Не запускает внешний процесс, работает с текстом напрямую"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""
    
    def _parse_output(self, content: str, file_path: str) -> List[Issue]:
        """Анализирует содержимое файла используя регулярные выражения"""
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
                        message=f"[{pattern_name}] {message}",
                    )
                    issues.append(issue)
        
        return issues


class SecurityAnalyser(BaseAnalyser):
    """Анализатор для обнаружения потенциальных проблем безопасности"""
    
    ext = "any"
    name = "Security"
    
    # Вредоносные паттерны
    SECURITY_PATTERNS = {
        "hardcoded_password": (
            r"password\s*=\s*['\"]",
            Severity.CRIT,
            "Hardcoded password detected"
        ),
        "hardcoded_api_key": (
            r"(api_key|apikey|api-key)\s*=\s*['\"]",
            Severity.CRIT,
            "Hardcoded API key detected"
        ),
        "sql_injection": (
            r"(execute|query|exec)\s*\(\s*f['\"].*{",
            Severity.ERR,
            "Potential SQL injection vulnerability"
        ),
        "eval_usage": (
            r"\beval\s*\(",
            Severity.ERR,
            "Use of eval() is dangerous"
        ),
        "pickle_usage": (
            r"pickle\.(load|loads)",
            Severity.ERR,
            "Unsafe use of pickle"
        ),
        "weak_hash": (
            r"(md5|sha1)\(",
            Severity.WARN,
            "Weak hash function used"
        ),
    }
    
    def _run_linter(self, file_path: str) -> str:
        """Читает содержимое файла"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""
    
    def _parse_output(self, content: str, file_path: str) -> List[Issue]:
        """Анализирует содержимое на проблемы безопасности"""
        issues = []
        
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for vuln_name, (pattern, severity, message) in self.SECURITY_PATTERNS.items():
                if re.search(pattern, line, re.IGNORECASE):
                    issue = Issue(
                        id=None,
                        run_id=None,
                        file_path=file_path,
                        line_start=line_num,
                        line_end=line_num,
                        severity=severity,
                        message=f"[security:{vuln_name}] {message}",
                    )
                    issues.append(issue)
        
        return issues


class ComplexityAnalyser(BaseAnalyser):
    """Анализатор для обнаружения сложного кода"""
    
    ext = ".py"
    name = "Complexity"
    
    def _run_linter(self, file_path: str) -> str:
        """Читает содержимое файла"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""
    
    def _parse_output(self, content: str, file_path: str) -> List[Issue]:
        """Анализирует сложность кода"""
        issues = []
        
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Обнаружение вложенных циклов
            indent_level = len(line) - len(line.lstrip())
            indent_tabs = indent_level // 4
            
            if indent_tabs >= 3:
                if re.search(r'\b(for|while|if)\b', line):
                    issue = Issue(
                        id=None,
                        run_id=None,
                        file_path=file_path,
                        line_start=line_num,
                        line_end=line_num,
                        severity=Severity.WARN,
                        message=f"[complexity] Deeply nested code (indent level {indent_tabs})",
                    )
                    issues.append(issue)
            
            # Обнаружение длинных функций
            if re.search(r'^def\s+\w+\(', line):
                # Подсчитываем строки функции
                func_lines = 0
                for i in range(line_num, len(lines)):
                    next_line = lines[i]
                    if i > line_num and next_line and next_line[0] not in (' ', '\t'):
                        break
                    func_lines += 1
                
                if func_lines > 50:
                    issue = Issue(
                        id=None,
                        run_id=None,
                        file_path=file_path,
                        line_start=line_num,
                        line_end=line_num,
                        severity=Severity.WARN,
                        message=f"[complexity] Function is too long ({func_lines} lines)",
                    )
                    issues.append(issue)
        
        return issues
