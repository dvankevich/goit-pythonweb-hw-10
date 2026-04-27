from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="567234")
    POSTGRES_DB: str = Field(default="contacts_db")
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)

    JWT_SECRET: str = Field(default="your_secret_key")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_SECONDS: int = 3600
    LOG_LEVEL: str = "INFO"

    CORS_ALLOWED_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:5173"
    )

    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ALLOWED_ORIGINS.split(",")]

    # async for FastAPI/SQLAlchemy
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # sync for Alembic
    @property
    def SYNC_DATABASE_URL(self) -> str:
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def DB_ECHO(self) -> bool:
        return self.LOG_LEVEL == "DEBUG"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=True
    )


settings = Settings()
