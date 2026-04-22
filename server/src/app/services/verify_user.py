from ..interfaces.auth_client import IAuthClient
from ..interfaces.uow import IUnitOfWork


class VerifyUserService:
    """Application service для верификации пользователя (Clean Architecture)"""
    
    def __init__(self, auth_client: IAuthClient, uow: IUnitOfWork):
        self.auth_client = auth_client
        self.uow = uow

    def verify_token(self, token: str, timeout: int = 10) -> bool:
        """Проверяет и верифицирует токен пользователя"""
        try:
            user:str = self.auth_client.verify(token, timeout)
            
            # Опционально: попытаться записать его к себе
            # with self.uow:
            #     self.uow.users.ensure(user)
            
            return True
        except Exception as e:
            print(f"Token verification error: {e}")
            return False
