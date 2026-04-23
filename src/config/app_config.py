from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Визначаємо шлях до кореня проекту (де лежить .env)
# Path(__file__).resolve() — це шлях до поточного файлу settings.py
# .parent.parent — піднімаємось на рівні вгору до кореня
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    LOG_LEVEL: str = "INFO"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        # Використовуємо абсолютний шлях
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )



settings = Settings()

