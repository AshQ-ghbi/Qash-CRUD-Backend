"""FastAPI application entry point (backend: app/main.py).

Run with:  uvicorn app.main:app --reload
"""
from fastapi import FastAPI

from app import models  # noqa: F401  (ensures the Student table is registered on Base)
from app.config import settings
from app.database import Base, engine
from app.routers import ai_query, students

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.include_router(students.router)
app.include_router(ai_query.router)


@app.get("/", tags=["Health"])
def root():
    return {"message": f"{settings.APP_NAME} is running", "docs": "/docs"}
