from typing import Optional
from datetime import date, timedelta
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from src.models import Contact
from src.schemas.contact import ContactCreate, ContactUpdate


def get_all(
    db: Session,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    upcoming_birthdays: bool = False,
):

    stmt = select(Contact)

    if first_name:
        stmt = stmt.where(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        stmt = stmt.where(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        stmt = stmt.where(Contact.email.ilike(f"%{email}%"))

    # birthday filter
    if upcoming_birthdays:
        today = date.today()
        # Generate a list of "MM-DD" strings for the next 7 days
        upcoming_dates = [
            (today + timedelta(days=i)).strftime("%m-%d") for i in range(7)
        ]

        # ignore year
        stmt = stmt.where(func.to_char(Contact.birthday, "MM-DD").in_(upcoming_dates))

    return db.scalars(stmt).all()


def get_by_id(db: Session, contact_id: int):
    return db.get(Contact, contact_id)


def get_by_email(db: Session, email: str):
    stmt = select(Contact).where(Contact.email == email)
    return db.execute(stmt).scalar_one_or_none()


def create(db: Session, contact_data: ContactCreate):
    db_contact = Contact(**contact_data.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update(
    db: Session, contact_id: int, contact_data: ContactUpdate
) -> Optional[Contact]:
    db_contact = db.get(Contact, contact_id)
    if not db_contact:
        return None

    update_data = contact_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_contact, key, value)

    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete(db: Session, contact_id: int) -> bool:
    contact = get_by_id(db, contact_id)
    if contact:
        db.delete(contact)
        db.commit()
        return True
    return False
