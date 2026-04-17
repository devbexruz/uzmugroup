from typing import Generator
from app.db.session import SessionLocal

def get_db() -> Generator:
    """Ma'lumotlar bazasiga seansni yaratib oxirida yopib beradi"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
