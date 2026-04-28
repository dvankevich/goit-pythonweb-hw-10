from __future__ import annotations
from typing import TYPE_CHECKING, List
from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql.sqltypes import DateTime

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.contact import Contact


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    avatar: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    confirmed: Mapped[bool] = mapped_column(default=False)
    # confirmed: Mapped[bool] = mapped_column(default=False, server_default=sa.text("false")) # check on new database
    contacts: Mapped[List["Contact"]] = relationship(
        "Contact", back_populates="user", cascade="all, delete-orphan"
    )
