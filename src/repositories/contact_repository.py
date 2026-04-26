from typing import Optional, List
from datetime import date, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Contact
from src.schemas.contact import ContactCreate, ContactUpdate


async def get_all(
    db: AsyncSession,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    upcoming_birthdays: bool = False,
) -> List[Contact]:

    stmt = select(Contact)

    if first_name:
        stmt = stmt.where(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        stmt = stmt.where(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        stmt = stmt.where(Contact.email.ilike(f"%{email}%"))

    if upcoming_birthdays:
        today = date.today()
        upcoming_dates = [
            (today + timedelta(days=i)).strftime("%m-%d") for i in range(7)
        ]
        stmt = stmt.where(func.to_char(Contact.birthday, "MM-DD").in_(upcoming_dates))

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_by_id(db: AsyncSession, contact_id: int) -> Optional[Contact]:
    return await db.get(Contact, contact_id)


async def get_by_email(db: AsyncSession, email: str) -> Optional[Contact]:
    stmt = select(Contact).where(Contact.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create(db: AsyncSession, contact_data: ContactCreate) -> Contact:
    db_contact = Contact(**contact_data.model_dump())
    db.add(db_contact)
    await db.commit()
    await db.refresh(db_contact)
    return db_contact


async def update(
    db: AsyncSession, contact_id: int, contact_data: ContactUpdate
) -> Optional[Contact]:
    db_contact = await db.get(Contact, contact_id)
    if not db_contact:
        return None

    update_data = contact_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_contact, key, value)

    await db.commit()
    await db.refresh(db_contact)
    return db_contact


async def delete(db: AsyncSession, contact_id: int) -> bool:
    contact = await get_by_id(db, contact_id)
    if contact:
        await db.delete(contact)
        await db.commit()
        return True
    return False
