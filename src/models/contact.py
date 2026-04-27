from __future__ import (
    annotations,
)
from typing import TYPE_CHECKING
from datetime import date

from sqlalchemy import String, Date, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.base import Base

if TYPE_CHECKING:
    from src.models.user import User


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="contacts")
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), index=True)
    phone: Mapped[str] = mapped_column(String(20))
    birthday: Mapped[date] = mapped_column(Date)
    additional_info: Mapped[str | None] = mapped_column(Text, nullable=True)
