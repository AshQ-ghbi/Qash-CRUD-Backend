"""Seed the students database with 5 dummy records (project root: seed_data.py).

Usage (from the project root):  python seed_data.py

All records are fictional. Emails use the reserved example.com domain and phone
numbers are obviously fake placeholders. The script is idempotent: students whose
email already exists are skipped, so it is safe to run more than once.
"""
from datetime import date

from app import models
from app.database import Base, SessionLocal, engine

DUMMY_STUDENTS = [
    {
        "name": "Aarav Demo",
        "date_of_birth": date(2003, 5, 14),
        "email": "aarav.demo@example.com",
        "phone": "9000000001",
        "course": "Computer Science",
        "address": "101 Sample Street, Demo City",
        "enrollment_date": date(2024, 7, 1),
    },
    {
        "name": "Diya Sample",
        "date_of_birth": date(2002, 11, 3),
        "email": "diya.sample@example.com",
        "phone": "9000000002",
        "course": "Electronics Engineering",
        "address": "202 Test Avenue, Sample Town",
        "enrollment_date": date(2024, 7, 1),
    },
    {
        "name": "Kabir Test",
        "date_of_birth": date(2004, 1, 22),
        "email": "kabir.test@example.com",
        "phone": "9000000003",
        "course": "Computer Science",
        "address": None,
        "enrollment_date": date(2025, 7, 15),
    },
    {
        "name": "Meera Placeholder",
        "date_of_birth": date(2003, 8, 9),
        "email": "meera.placeholder@example.com",
        "phone": "9000000004",
        "course": "Mechanical Engineering",
        "address": "404 Mock Lane, Example Nagar",
        "enrollment_date": date(2025, 1, 10),
    },
    {
        "name": "Rohan Fictional",
        "date_of_birth": date(2001, 12, 30),
        "email": "rohan.fictional@example.com",
        "phone": "9000000005",
        "course": None,
        "address": "505 Dummy Road, Test Colony",
        "enrollment_date": date(2024, 1, 20),
    },
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    inserted, skipped = 0, 0
    try:
        for record in DUMMY_STUDENTS:
            exists = (
                db.query(models.Student)
                .filter(models.Student.email == record["email"])
                .first()
            )
            if exists:
                skipped += 1
                continue
            db.add(models.Student(**record))
            inserted += 1
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
    print(f"Seeding complete: {inserted} inserted, {skipped} already present.")


if __name__ == "__main__":
    seed()
