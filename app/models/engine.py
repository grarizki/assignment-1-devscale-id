from sqlmodel import create_engine, Session
from app.core.settings import settings

# Database URL from environment or default to SQLite
engine = create_engine(settings.database_url, echo=True)


def db_session():
    with Session(engine) as session:
        yield session
