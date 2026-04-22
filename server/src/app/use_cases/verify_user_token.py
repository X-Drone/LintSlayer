from ..interfaces.auth_client import IAuthClient


class VerifyUserTokenUseCase:
    """Use case для верификации токена пользователя"""
    
    def __init__(self, auth_client: IAuthClient):
        self.auth_client = auth_client


    def __call__(self, token: str, timeout: int = 10) -> str | None:
        """Проверяет и верифицирует токен пользователя"""
        try:
            user:str = self.auth_client.verify(token, timeout)
            
            # Опционально: попытаться записать его к себе
            # with self.uow:
            #     self.uow.users.ensure(user)
            
            return user
        except Exception as e:
            print(f"Token verification error: {e}")
            return
