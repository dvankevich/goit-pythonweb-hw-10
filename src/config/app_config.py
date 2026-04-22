from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # ігнорувати інші змінні в .env, які не описані в класі
    )


settings = Settings()

DATABASE_CONNECT_URL = settings.DATABASE_URL