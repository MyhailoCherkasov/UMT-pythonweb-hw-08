from sqlalchemy import Column, Integer, String, Date
from database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    phone = Column(String(30), nullable=False)
    birthday = Column(Date, nullable=False)
    additional_data = Column(String(500), nullable=True)
