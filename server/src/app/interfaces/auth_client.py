from abc import ABC, abstractmethod

__all__ = ["IAuthClient", "InvalidTokenError", "AuthTimeoutError", "AuthServiceError"]


class AuthError(Exception):
    pass


class InvalidTokenError(AuthError):
    pass


class AuthTimeoutError(AuthError):
    pass


class AuthServiceError(AuthError):
    pass


class IAuthClient(ABC):
    @abstractmethod
    def verify(self, token: str, timeout: int) -> str: ...
