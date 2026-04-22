from datetime import date
from sqlalchemy import String, Date, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(20))
    birthday: Mapped[date] = mapped_column(Date)
    additional_info: Mapped[str | None] = mapped_column(Text, nullable=True)
