"""
Database initialization script
Run this to create all tables in the database
"""
from sqlmodel import SQLModel
from app.models.engine import engine
from app.models.database import Stocks  # Import all models here


def init_db():
    """Create all database tables"""
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()
