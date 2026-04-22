from enum import Enum

__all__ = ["Status", "Severity"]


class Status(Enum):
    PENDING = 0
    RUNNING = 1
    COMPLETED = 2
    FAILED = 3


class Severity(Enum):
    INFO = 0
    WARN = 1
    ERR = 2
    CRIT = 3
