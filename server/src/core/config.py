from pydantic_settings import BaseSettings
from pydantic import model_validator
from typing import Optional

class Settings(BaseSettings):
    # Режим разработки
    debug: bool = False

    auth_url: str = "http://localhost:3003/auth/"
    
    # База данных
    database_url: str
    database_pool_size: int = 5
    database_pool_timeout: int = 30
    
    # Настройки для локальной разработки
    

    @model_validator(mode="after")
    def assemble_url(self):
        if self.debug:
            self.database_url = (
                "sqlite:///./dev.db"
                # "sqlite+aiosqlite:///./dev.db"
            )
        return self
    
    class Config:
        env_file = ".env",
        extra="ignore"
