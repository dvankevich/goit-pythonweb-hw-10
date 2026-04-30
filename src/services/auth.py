import bcrypt
from datetime import datetime, timedelta, UTC
from typing import Optional

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from src.db.session import get_db
from src.config.app_config import settings
from src.services.users import UserService


class Hash:
    def verify_password(self, plain_password: str, hashed_password: str):
        password_byte = plain_password.encode("utf-8")
        hashed_byte = hashed_password.encode("utf-8")
        return bcrypt.checkpw(password_byte, hashed_byte)

    def get_password_hash(self, password: str):
        # Обрізаємо до 72 байт для безпеки bcrypt
        password_byte = password.encode("utf-8")[:72]
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password_byte, salt).decode("utf-8")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ====================== JWT TOKENS ======================

async def create_access_token(data: dict, expires_delta: Optional[int] = None):
    """Створення access токена для авторизації"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + timedelta(seconds=expires_delta)
    else:
        expire = datetime.now(UTC) + timedelta(seconds=settings.JWT_EXPIRATION_SECONDS)

    to_encode.update({"exp": expire})

    # Важливо: розпаковуємо SecretStr в звичайний рядок
    secret_key = settings.JWT_SECRET.get_secret_value()

    encoded_jwt = jwt.encode(
        to_encode, secret_key, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_email_token(data: dict):
    """Створення токена для підтвердження email"""
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=7)
    to_encode.update({"iat": datetime.now(UTC), "exp": expire})

    # Розпаковуємо SecretStr
    secret_key = settings.JWT_SECRET.get_secret_value()

    token = jwt.encode(to_encode, secret_key, algorithm=settings.JWT_ALGORITHM)
    return token


async def get_email_from_token(token: str):
    """Отримання email з токена підтвердження"""
    try:
        secret_key = settings.JWT_SECRET.get_secret_value()

        payload = jwt.decode(
            token, secret_key, algorithms=[settings.JWT_ALGORITHM]
        )
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Неправильний токен для перевірки електронної пошти",
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Неправильний токен для перевірки електронної пошти",
        )


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    """Отримання поточного користувача з JWT токена"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        secret_key = settings.JWT_SECRET.get_secret_value()

        payload = jwt.decode(
            token, secret_key, algorithms=[settings.JWT_ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_service = UserService(db)
    user = await user_service.get_user_by_username(username)
    if user is None:
        raise credentials_exception

    return user