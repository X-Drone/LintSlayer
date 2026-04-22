"""
JavaScript/TypeScript анализаторы (ESLint, Prettier, TypeScript)
"""

import json
import re
from typing import List
from domain.entities import Issue
from domain.values import Severity
from .base import BaseAnalyser


class ESLintAnalyser(BaseAnalyser):
    """Анализатор JavaScript/TypeScript кода используя ESLint"""
    
    ext = ".js"
    name = "eslint"
    
    def _run_linter(self, file_path: str) -> str:
        """Запускает eslint"""
        command = [
            "eslint",
            "--format=json",
            "--no-eslintrc",  # Используем дефолтные правила
            file_path,
        ]
        return self._run_command(command)
    
    def _parse_output(self, output: str, file_path: str) -> List[Issue]:
        """Парсит JSON вывод eslint"""
        issues = []
        
        try:
            if not output.strip():
                return issues
            
            data = json.loads(output)
            
            for file_result in data:
                for message in file_result.get("messages", []):
                    try:
                        severity = Severity.WARN
                        if message.get("severity") == 2:
                            severity = Severity.ERR
                        elif message.get("severity") == 1:
                            severity = Severity.WARN
                        
                        issue = Issue(
                            id=None,
                            run_id=None,
                            file_path=file_path,
                            line_start=message.get("line", 0),
                            line_end=message.get("line", 0),
                            severity=severity,
                            message=f"[{message.get('ruleId', 'unknown')}] {message.get('message', '')}",
                        )
                        issues.append(issue)
                    except Exception as e:
                        print(f"Error parsing eslint message: {e}")
                        continue
        
        except json.JSONDecodeError:
            print(f"Failed to parse eslint output as JSON")
        
        return issues


class TSLintAnalyser(BaseAnalyser):
    """Анализатор TypeScript кода используя tslint"""
    
    ext = ".ts"
    name = "tslint"
    
    def _run_linter(self, file_path: str) -> str:
        """Запускает tslint"""
        command = [
            "tslint",
            "--format=json",
            file_path,
        ]
        return self._run_command(command)
    
    def _parse_output(self, output: str, file_path: str) -> List[Issue]:
        """Парсит JSON вывод tslint"""
        issues = []
        
        try:
            if not output.strip():
                return issues
            
            data = json.loads(output)
            
            for item in data:
                try:
                    severity = self._map_severity(item.get("severity", "warning"))
                    
                    issue = Issue(
                        id=None,
                        run_id=None,
                        file_path=file_path,
                        line_start=item.get("startPosition", {}).get("line", 0) + 1,
                        line_end=item.get("endPosition", {}).get("line", 0) + 1,
                        severity=severity,
                        message=f"[{item.get('ruleName', 'unknown')}] {item.get('failure', '')}",
                    )
                    issues.append(issue)
                except Exception as e:
                    print(f"Error parsing tslint item: {e}")
                    continue
        
        except json.JSONDecodeError:
            print(f"Failed to parse tslint output as JSON")
        
        return issues


class PrettierAnalyser(BaseAnalyser):
    """Анализатор форматирования кода используя Prettier"""
    
    ext = ".js"
    name = "prettier"
    
    def _run_linter(self, file_path: str) -> str:
        """Проверяет форматирование с prettier"""
        command = [
            "prettier",
            "--check",
            file_path,
        ]
        return self._run_command(command)
    
    def _parse_output(self, output: str, file_path: str) -> List[Issue]:
        """Парсит вывод prettier"""
        issues = []
        
        # Prettier просто выводит имя файла если не отформатирован
        if file_path in output and "not" in output.lower():
            issue = Issue(
                id=None,
                run_id=None,
                file_path=file_path,
                line_start=1,
                line_end=1,
                severity=Severity.WARN,
                message="Code is not formatted according to Prettier rules",
            )
            issues.append(issue)
        
        return issues
