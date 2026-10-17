"""Students CRUD endpoints (backend: app/routers/students.py)."""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/students", tags=["Students"])


def _not_found(student_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Student with id {student_id} not found",
    )


@router.post("/", response_model=schemas.StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_student(db, student)
    except crud.DuplicateEmailError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/", response_model=List[schemas.StudentOut])
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    name: Optional[str] = Query(None, description="Partial, case-insensitive name match"),
    course: Optional[str] = Query(None, description="Partial, case-insensitive course match"),
    email: Optional[str] = Query(None, description="Partial, case-insensitive email match"),
    db: Session = Depends(get_db),
):
    return crud.get_students(db, skip=skip, limit=limit, name=name, course=course, email=email)


@router.get("/{student_id}", response_model=schemas.StudentOut)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id)
    if db_student is None:
        raise _not_found(student_id)
    return db_student


def _apply_update(student_id: int, student: schemas.StudentUpdate, db: Session):
    try:
        db_student = crud.update_student(db, student_id, student)
    except crud.DuplicateEmailError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    if db_student is None:
        raise _not_found(student_id)
    return db_student


@router.put("/{student_id}", response_model=schemas.StudentOut)
def update_student_put(
    student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)
):
    return _apply_update(student_id, student, db)


@router.patch("/{student_id}", response_model=schemas.StudentOut)
def update_student_patch(
    student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)
):
    return _apply_update(student_id, student, db)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    if crud.delete_student(db, student_id) is None:
        raise _not_found(student_id)
    return None
