from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    class Config:
        env_file=".env"
        extra = "ignore"

@lru_cache
def get_settings() -> Settings:
    return Settings()