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
    """Анализатор кода Python используя Flake8"""
    
    ext = ".py"
    name = "flake8"
    
    def _run_linter(self, file_path: str) -> str:
        """Запускает flake8"""
        command = [
            "flake8",
            "--format=json",
            file_path,
        ]
        return self._run_command(command)
    
    def _parse_output(self, output: str, file_path: str) -> List[Issue]:
        """Парсит JSON вывод flake8"""
        issues = []
        
        try:
            if not output.strip():
                return issues
            
            data = json.loads(output)
            
            for item in data:
                try:
                    # Flake8 коды: E = Error, W = Warning, F = Fatal
                    code = item.get("code", "E")
                    if code.startswith("E"):
                        severity = Severity.ERR
                    elif code.startswith("F"):
                        severity = Severity.CRIT
                    else:
                        severity = Severity.WARN
                    
                    issue = Issue(
                        id=None,
                        run_id=None,
                        file_path=file_path,
                        line_start=item.get("line_number", 0),
                        line_end=item.get("line_number", 0),
                        severity=severity,
                        message=f"[{item.get('code', 'unknown')}] {item.get('text', '')}",
                    )
                    issues.append(issue)
                except Exception as e:
                    print(f"Error parsing flake8 item: {e}")
                    continue
        
        except json.JSONDecodeError:
            print(f"Failed to parse flake8 output as JSON")
        
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
