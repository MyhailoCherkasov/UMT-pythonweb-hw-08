from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from schemas import ContactCreate, ContactUpdate, ContactResponse
import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contacts REST API")


@app.post("/contacts/", response_model=ContactResponse, status_code=201)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)


@app.get("/contacts/", response_model=list[ContactResponse])
def read_contacts(
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_contacts(db, skip=skip, limit=limit, search=search)


@app.get("/contacts/birthdays", response_model=list[ContactResponse])
def upcoming_birthdays(db: Session = Depends(get_db)):
    return crud.get_upcoming_birthdays(db)


@app.get("/contacts/{contact_id}", response_model=ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact(db, contact_id)

    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    return contact


@app.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    updated_contact = crud.update_contact(db, contact_id, contact)

    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    return updated_contact


@app.delete("/contacts/{contact_id}", response_model=ContactResponse)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    deleted_contact = crud.delete_contact(db, contact_id)

    if deleted_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    return deleted_contact
