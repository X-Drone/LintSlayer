"""
Python анализаторы (Pylint, Flake8, Pyright)
"""

import re
import subprocess
import json
from typing import List
from domain.entities import Issue
from domain.values import Severity
from .base import BaseAnalyser


class PylintAnalyser(BaseAnalyser):
    """Анализатор кода Python используя Pylint"""
    
    ext = ".py"
    name = "pylint"
    
    def _run_linter(self, file_path: str) -> str:
        """Запускает pylint"""
        command = [
            "pylint",
            "--output-format=json",
            "--exit-zero",  # Не ошибка, если pylint найдет проблемы
            file_path,
        ]
        return self._run_command(command)
    
    def _parse_output(self, output: str, file_path: str) -> List[Issue]:
        """Парсит JSON вывод pylint"""
        issues = []
        
        try:
            if not output.strip():
                return issues
            
            data = json.loads(output)
            
            for item in data:
                try:
                    severity = self._map_severity(item.get("type", "warning"))
                    
                    issue = Issue(
                        id=None,
                        run_id=None,  # Будет установлено при сохранении
                        file_path=file_path,
                        line_start=item.get("line", 0),
                        line_end=item.get("line", 0),
                        severity=severity,
                        message=f"[{item.get('symbol', 'unknown')}] {item.get('message', '')}",
                    )
                    issues.append(issue)
                except Exception as e:
                    print(f"Error parsing pylint item: {e}")
                    continue
        
        except json.JSONDecodeError:
            print(f"Failed to parse pylint output as JSON")
        
        return issues


class Flake8Analyser(BaseAnalyser):
    """Анализатор кода Python через flake8"""
    
    ext = ".py"
    name = "flake8"

    SEPARATOR = "|||"

    def _run_linter(self, file_path: str) -> str:
        """Запускает flake8 с кастомным форматом"""
        command = [
            "flake8",
            f"--format=%(path)s{self.SEPARATOR}%(row)d{self.SEPARATOR}%(col)d{self.SEPARATOR}%(code)s{self.SEPARATOR}%(text)s",
            file_path,
        ]
        return self._run_command(command)

    def _parse_output(self, output: str, file_path: str) -> List[Issue]:
        """Парсит вывод flake8"""
        issues: List[Issue] = []

        if not output.strip():
            return issues

        for line in output.splitlines():
            try:
                parts = line.split(self.SEPARATOR)

                # защита от мусора
                if len(parts) != 5:
                    continue

                path, row, col, code, text = parts

                # --- severity mapping ---
                if code.startswith("F"):
                    severity = Severity.CRIT
                elif code.startswith("E"):
                    severity = Severity.ERR
                else:
                    severity = Severity.WARN

                issue = Issue(
                    id=None,
                    run_id=None,
                    file_path=path or file_path,
                    line_start=int(row),
                    line_end=int(row),
                    severity=severity,
                    message=f"[{code}] {text}",
                )

                issues.append(issue)

            except Exception as e:
                # не убиваем весь анализ из-за одной строки
                print(f"Flake8 parse error: {e} | line: {line}")
                continue

        return issues


class PyrightAnalyser(BaseAnalyser):
    """Анализатор типов Python используя Pyright"""
    
    ext = ".py"
    name = "pyright"
    
    def _run_linter(self, file_path: str) -> str:
        """Запускает pyright"""
        command = [
            "pyright",
            "--outputjson",
            file_path,
        ]
        return self._run_command(command)
    
    def _parse_output(self, output: str, file_path: str) -> List[Issue]:
        """Парсит JSON вывод pyright"""
        issues = []
        
        try:
            if not output.strip():
                return issues
            
            data = json.loads(output)
            
            # Pyright возвращает results в массиве
            for result in data.get("generalDiagnostics", []):
                try:
                    severity = self._map_severity(result.get("severity", "warning"))
                    
                    range_info = result.get("range", {})
                    start = range_info.get("start", {})
                    end = range_info.get("end", {})
                    
                    issue = Issue(
                        id=None,
                        run_id=None,
                        file_path=file_path,
                        line_start=start.get("line", 0) + 1,
                        line_end=end.get("line", 0) + 1,
                        severity=severity,
                        message=result.get("message", "Unknown error"),
                    )
                    issues.append(issue)
                except Exception as e:
                    print(f"Error parsing pyright item: {e}")
                    continue
        
        except json.JSONDecodeError:
            print(f"Failed to parse pyright output as JSON")
        
        return issues
