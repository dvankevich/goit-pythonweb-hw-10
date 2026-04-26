from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"  # Алгоритм шифрування токенів
    JWT_EXPIRATION_SECONDS: int = 3600  # Час дії токена (1 година)    
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore", 
        case_sensitive=True
    )


settings = Settings() # type: ignore
