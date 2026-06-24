from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import or_, extract
from models import Contact
from schemas import ContactCreate, ContactUpdate


def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts(db: Session, skip: int = 0, limit: int = 100, search: str | None = None):
    query = db.query(Contact)

    if search:
        search_value = f"%{search}%"
        query = query.filter(
            or_(
                Contact.first_name.ilike(search_value),
                Contact.last_name.ilike(search_value),
                Contact.email.ilike(search_value),
            )
        )

    return query.offset(skip).limit(limit).all()


def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()


def update_contact(db: Session, contact_id: int, contact: ContactUpdate):
    db_contact = get_contact(db, contact_id)

    if not db_contact:
        return None

    for key, value in contact.model_dump().items():
        setattr(db_contact, key, value)

    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)

    if not db_contact:
        return None

    db.delete(db_contact)
    db.commit()
    return db_contact


def get_upcoming_birthdays(db: Session):
    today = date.today()
    dates = [today + timedelta(days=i) for i in range(7)]

    conditions = [
        (extract("month", Contact.birthday) == d.month)
        & (extract("day", Contact.birthday) == d.day)
        for d in dates
    ]

    return db.query(Contact).filter(or_(*conditions)).all()
