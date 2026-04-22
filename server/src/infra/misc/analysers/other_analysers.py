"""
Java, Go, Rust анализаторы
"""

import json
import re
from typing import List
from domain.entities import Issue
from domain.values import Severity
from .base import BaseAnalyser


class CheckstyleAnalyser(BaseAnalyser):
    """Анализатор Java кода используя Checkstyle"""
    
    ext = ".java"
    name = "checkstyle"
    
    def _run_linter(self, file_path: str) -> str:
        """Запускает checkstyle"""
        command = [
            "checkstyle",
            "-f=json",
            file_path,
        ]
        return self._run_command(command)
    
    def _parse_output(self, output: str, file_path: str) -> List[Issue]:
        """Парсит JSON вывод checkstyle"""
        issues = []
        
        try:
            if not output.strip():
                return issues
            
            data = json.loads(output)
            
            for file_info in data:
                for violation in file_info.get("violations", []):
                    try:
                        severity = self._map_severity(violation.get("severity", "warning"))
                        
                        issue = Issue(
                            id=None,
                            run_id=None,
                            file_path=file_path,
                            line_start=violation.get("line", 0),
                            line_end=violation.get("line", 0),
                            severity=severity,
                            message=f"[{violation.get('rule', 'unknown')}] {violation.get('message', '')}",
                        )
                        issues.append(issue)
                    except Exception as e:
                        print(f"Error parsing checkstyle violation: {e}")
                        continue
        
        except json.JSONDecodeError:
            print(f"Failed to parse checkstyle output as JSON")
        
        return issues


class GoLintAnalyser(BaseAnalyser):
    """Анализатор Go кода используя golangci-lint"""
    
    ext = ".go"
    name = "golangci-lint"
    
    def _run_linter(self, file_path: str) -> str:
        """Запускает golangci-lint"""
        command = [
            "golangci-lint",
            "run",
            "--out-format=json",
            file_path,
        ]
        return self._run_command(command)
    
    def _parse_output(self, output: str, file_path: str) -> List[Issue]:
        """Парсит JSON вывод golangci-lint"""
        issues = []
        
        try:
            if not output.strip():
                return issues
            
            data = json.loads(output)
            
            for issue_data in data.get("Issues", []):
                try:
                    severity = self._map_severity(issue_data.get("Severity", "warning"))
                    
                    issue = Issue(
                        id=None,
                        run_id=None,
                        file_path=file_path,
                        line_start=issue_data.get("Line", 0),
                        line_end=issue_data.get("Line", 0),
                        severity=severity,
                        message=f"[{issue_data.get('FromLinter', 'unknown')}] {issue_data.get('Text', '')}",
                    )
                    issues.append(issue)
                except Exception as e:
                    print(f"Error parsing golangci-lint issue: {e}")
                    continue
        
        except json.JSONDecodeError:
            print(f"Failed to parse golangci-lint output as JSON")
        
        return issues


class ClippyAnalyser(BaseAnalyser):
    """Анализатор Rust кода используя clippy"""
    
    ext = ".rs"
    name = "clippy"
    
    def _run_linter(self, file_path: str) -> str:
        """Запускает clippy через cargo"""
        command = [
            "cargo",
            "clippy",
            "--message-format=json",
            file_path,
        ]
        return self._run_command(command)
    
    def _parse_output(self, output: str, file_path: str) -> List[Issue]:
        """Парсит JSON вывод clippy"""
        issues = []
        
        try:
            for line in output.strip().split('\n'):
                if not line.strip():
                    continue
                
                try:
                    data = json.loads(line)
                    
                    # Clippy выводит compiler messages
                    if data.get("level") in ["warning", "error", "note"]:
                        severity = self._map_severity(data.get("level", "warning"))
                        
                        message = data.get("message", "Unknown")
                        spans = data.get("spans", [])
                        
                        if spans:
                            span = spans[0]
                            issue = Issue(
                                id=None,
                                run_id=None,
                                file_path=file_path,
                                line_start=span.get("line_start", 0),
                                line_end=span.get("line_end", 0),
                                severity=severity,
                                message=message,
                            )
                            issues.append(issue)
                
                except json.JSONDecodeError:
                    continue
        
        except Exception as e:
            print(f"Error parsing clippy output: {e}")
        
        return issues
