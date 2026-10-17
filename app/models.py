"""SQLAlchemy ORM models (backend: app/models.py)."""
from datetime import date

from sqlalchemy import Column, Date, Integer, String

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=False)
    course = Column(String, nullable=True)
    address = Column(String, nullable=True)
    enrollment_date = Column(Date, nullable=False, default=date.today)

    def __repr__(self) -> str:
        return f"<Student id={self.id} name={self.name!r} email={self.email!r}>"
