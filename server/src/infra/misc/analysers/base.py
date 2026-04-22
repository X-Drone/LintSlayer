"""
Base Analyser implementation с поддержкой различных линтеров
"""

import subprocess
import json
import re
from abc import ABC, abstractmethod
from app.interfaces.analyser import IAnalyser
from typing import Callable, List
from pathlib import Path
from domain.entities import Issue
from domain.values import Severity


class BaseAnalyser(IAnalyser):
    """Базовый класс для анализаторов"""
    
    ext: str  # Расширение файла, например ".py"
    name: str  # Имя анализатора, например "pylint"
    
    @abstractmethod
    def _run_linter(self, file_path: str) -> str:
        """Запускает линтер и возвращает результат"""
        pass
    
    @abstractmethod
    def _parse_output(self, output: str, file_path: str) -> List[Issue]:
        """Парсит вывод линтера и возвращает список Issues"""
        pass
    
    def analyse(self, file_path: str, on_complete: Callable[[List[Issue]], None]) -> None:
        """Главный метод для анализа файла"""
        try:
            output = self._run_linter(file_path)
            issues = self._parse_output(output, file_path)
            on_complete(issues)
        except Exception as e:
            print(f"Error analyzing {file_path} with {self.name}: {e}")
            on_complete([])
    
    def _map_severity(self, severity_str: str) -> Severity:
        """Преобразует строку уровня серьезности в enum"""
        severity_map = {
            "error": Severity.ERR,
            "warning": Severity.WARN,
            "info": Severity.INFO,
            "critical": Severity.CRIT,
            "fatal": Severity.CRIT,
        }
        return severity_map.get(severity_str.lower(), Severity.WARN)
    
    def _run_command(self, command: List[str]) -> str:
        """Выполняет command и возвращает output"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30,
            )
            return result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Command timed out: {' '.join(command)}")
        except FileNotFoundError:
            raise RuntimeError(f"Command not found: {command[0]}")
