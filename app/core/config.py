from pydantic import RedisDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: RedisDsn
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @computed_field
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return self.DATABASE_URL.replace(
            "postgresql://", "postgresql+asyncpg://"
        )

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="ignore"
    )

settings = Settings()