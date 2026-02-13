from sqlmodel import create_engine, Session
from app.core.settings import settings
import os

# Database URL from environment or default to SQLite
engine = create_engine(settings.database_url, echo=True)

def get_db():
    with Session(engine) as session:
        yield session
