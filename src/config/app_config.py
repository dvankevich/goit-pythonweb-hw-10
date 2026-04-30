from pydantic import Field, EmailStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from typing import List


class Settings(BaseSettings):
    # База даних
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: SecretStr = Field(default=SecretStr("567234"))
    POSTGRES_DB: str = Field(default="contacts_db")
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)

    # JWT
    JWT_SECRET: SecretStr = Field(
        default=SecretStr("your_super_secret_jwt_key_change_in_production")
    )
    JWT_ALGORITHM: str = Field(default="HS256")
    JWT_EXPIRATION_SECONDS: int = Field(default=3600)

    # Email - Brevo
    MAIL_USERNAME: EmailStr = Field(default="example@smtp-brevo.com")
    MAIL_PASSWORD: SecretStr = Field(default=SecretStr("xsmtpsib-default"))
    MAIL_FROM: EmailStr = Field(default="admin@dvankevich.pp.ua")
    MAIL_FROM_NAME: str = Field(default="Contacts API")
    MAIL_SERVER: str = Field(default="smtp-relay.brevo.com")
    MAIL_PORT: int = Field(default=587)
    MAIL_STARTTLS: bool = Field(default=True)
    MAIL_SSL_TLS: bool = Field(default=False)
    USE_CREDENTIALS: bool = Field(default=True)
    VALIDATE_CERTS: bool = Field(default=True)

    # Cloudinary
    CLD_NAME: str = Field(default="cloud")
    CLD_API_KEY: str = Field(default="")
    CLD_API_SECRET: SecretStr = Field(default=SecretStr("secret"))

    # Інше
    CORS_ALLOWED_ORIGINS: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173"
    )
    LOG_LEVEL: str = Field(default="DEBUG")

    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        return [
            origin.strip()
            for origin in self.CORS_ALLOWED_ORIGINS.split(",")
            if origin.strip()
        ]

    @property
    def DATABASE_URL(self) -> str:
        pwd = self.POSTGRES_PASSWORD.get_secret_value()
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{pwd}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        pwd = self.POSTGRES_PASSWORD.get_secret_value()
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{pwd}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


settings = Settings()
