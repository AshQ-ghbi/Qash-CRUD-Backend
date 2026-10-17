"""Pydantic v2 request/response schemas (backend: app/schemas.py)."""
import re
from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _validate_email(value: Optional[str]) -> Optional[str]:
    if value is None:
        return value
    value = value.strip().lower()
    if not _EMAIL_RE.match(value):
        raise ValueError("Invalid email address")
    return value


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    email: str = Field(..., max_length=254)
    phone: str = Field(..., min_length=5, max_length=20)
    course: Optional[str] = Field(default=None, max_length=100)
    address: Optional[str] = Field(default=None, max_length=255)

    @field_validator("email")
    @classmethod
    def check_email(cls, v: str) -> str:
        return _validate_email(v)


class StudentCreate(StudentBase):
    """Payload for creating a student. enrollment_date is set by the server (defaults to today)."""


class StudentUpdate(BaseModel):
    """All fields optional so the same schema serves PUT and PATCH."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    email: Optional[str] = Field(default=None, max_length=254)
    phone: Optional[str] = Field(default=None, min_length=5, max_length=20)
    course: Optional[str] = Field(default=None, max_length=100)
    address: Optional[str] = Field(default=None, max_length=255)

    @field_validator("email")
    @classmethod
    def check_email(cls, v: Optional[str]) -> Optional[str]:
        return _validate_email(v)


class StudentOut(StudentBase):
    id: int
    enrollment_date: date

    model_config = ConfigDict(from_attributes=True)
