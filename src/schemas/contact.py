from datetime import date
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    additional_info: str | None = None


class ContactCreate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    additional_info: Optional[str] = None
