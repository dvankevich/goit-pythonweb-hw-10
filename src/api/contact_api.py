from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.schemas.contact import ContactCreate, ContactResponse, ContactUpdate
from src.repositories import contact_repository

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    existing_contact = await contact_repository.get_by_email(db, email=contact.email)

    if existing_contact:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Contact with email '{contact.email}' already exists.",
        )

    # Додано await
    return await contact_repository.create(db, contact)


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    first_name: Optional[str] = Query(None, description="find by first name"),
    last_name: Optional[str] = Query(None, description="find by second name"),
    email: Optional[str] = Query(None, description="find by email"),
    upcoming_birthdays: bool = Query(
        False, description="Show only contacts with birthdays in the next 7 days"
    ),
    db: AsyncSession = Depends(get_db),
):
    # Додано await
    contacts = await contact_repository.get_all(
        db,
        first_name=first_name,
        last_name=last_name,
        email=email,
        upcoming_birthdays=upcoming_birthdays,
    )
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await contact_repository.get_by_id(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int, body: ContactUpdate, db: AsyncSession = Depends(get_db)
):
    if body.email:
        existing_contact = await contact_repository.get_by_email(db, email=body.email)

        if existing_contact and existing_contact.id != contact_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{body.email}' is already taken by another contact.",
            )

    updated_contact = await contact_repository.update(db, contact_id, body)

    if updated_contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with id {contact_id} not found",
        )

    return updated_contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    success = await contact_repository.delete(db, contact_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with id {contact_id} not found",
        )

    return None
