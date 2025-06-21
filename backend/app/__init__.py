from .database import SessionLocal
from fastapi import Depends

# Package initializer for backend.app

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()