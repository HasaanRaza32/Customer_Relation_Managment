from app.database import SessionLocal

# Dependency injection for FastAPI

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
