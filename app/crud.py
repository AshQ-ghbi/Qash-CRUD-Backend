"""Core CRUD logic (backend: app/crud.py).

Pure data-access layer: no HTTP concerns. Missing records are signalled by returning
None, duplicate emails by raising DuplicateEmailError; the router maps these to 404/409.
The read functions (get_student, get_students) are ORM-only and are reused read-only
by the Phase 3 AI service.
"""
from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas


class DuplicateEmailError(Exception):
    """Raised when an email is already registered to another student."""

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"A student with email '{email}' already exists")


def get_student(db: Session, student_id: int) -> Optional[models.Student]:
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def get_student_by_email(db: Session, email: str) -> Optional[models.Student]:
    return db.query(models.Student).filter(models.Student.email == email).first()


def get_students(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    course: Optional[str] = None,
    email: Optional[str] = None,
) -> List[models.Student]:
    """List students with pagination and optional case-insensitive partial filters."""
    query = db.query(models.Student)
    if name:
        query = query.filter(models.Student.name.ilike(f"%{name}%"))
    if course:
        query = query.filter(models.Student.course.ilike(f"%{course}%"))
    if email:
        query = query.filter(models.Student.email.ilike(f"%{email}%"))
    return query.order_by(models.Student.id).offset(skip).limit(limit).all()


def create_student(db: Session, student: schemas.StudentCreate) -> models.Student:
    if get_student_by_email(db, student.email):
        raise DuplicateEmailError(student.email)
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    try:
        db.commit()
    except IntegrityError:  # race condition: unique constraint hit between check and commit
        db.rollback()
        raise DuplicateEmailError(student.email)
    db.refresh(db_student)
    return db_student


def update_student(
    db: Session, student_id: int, student: schemas.StudentUpdate
) -> Optional[models.Student]:
    db_student = get_student(db, student_id)
    if db_student is None:
        return None

    data = student.model_dump(exclude_unset=True)

    new_email = data.get("email")
    if new_email and new_email != db_student.email:
        if get_student_by_email(db, new_email):
            raise DuplicateEmailError(new_email)

    # Required columns cannot be nulled out by an explicit null in the payload.
    for field, value in data.items():
        if value is None and field in {"name", "date_of_birth", "email", "phone"}:
            continue
        setattr(db_student, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateEmailError(new_email or db_student.email)
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int) -> Optional[models.Student]:
    db_student = get_student(db, student_id)
    if db_student is None:
        return None
    db.delete(db_student)
    db.commit()
    return db_student
