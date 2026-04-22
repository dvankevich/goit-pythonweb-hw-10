from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.schemas.contact import ContactCreate, ContactResponse, ContactUpdate
from src.repositories import contact_repository

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return contact_repository.create(db, contact)


@router.get("/", response_model=List[ContactResponse])
def read_contacts(
    first_name: Optional[str] = Query(None, description="find by first name"),
    last_name: Optional[str] = Query(None, description="find by second name"),
    email: Optional[str] = Query(None, description="find by email"),
    upcoming_birthdays: bool = Query(
        False, description="Show only contacts with birthdays in the next 7 days"
    ),
    db: Session = Depends(get_db),
):

    contacts = contact_repository.get_all(
        db,
        first_name=first_name,
        last_name=last_name,
        email=email,
        upcoming_birthdays=upcoming_birthdays,
    )
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = contact_repository.get_by_id(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, body: ContactUpdate, db: Session = Depends(get_db)):

    updated_contact = contact_repository.update(db, contact_id, body)

    if updated_contact is None:
        raise HTTPException(
            status_code=404, detail=f"Contact with id {contact_id} not found"
        )

    return updated_contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    success = contact_repository.delete(db, contact_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with id {contact_id} not found",
        )

    return None
