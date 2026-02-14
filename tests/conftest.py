"""
Pytest configuration and fixtures for the test suite
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.models.engine import get_db


@pytest.fixture(name="session")
def session_fixture():
    """
    Create a fresh in-memory SQLite database for each test.
    This ensures tests are isolated and don't affect each other.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Create a test client with dependency override for database session.
    This allows us to use the in-memory test database instead of the real one.
    """

    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_stock_data():
    """Sample stock data for testing"""
    return {
        "ticker": "BBCA",
        "name": "Bank Central Asia",
        "sector": "Banking",
        "current_price": 8500.0,
        "description": "Largest private bank in Indonesia",
    }


@pytest.fixture
def sample_stocks_list():
    """Multiple sample stocks for testing pagination and filtering"""
    return [
        {
            "ticker": "BBCA",
            "name": "Bank Central Asia",
            "sector": "Banking",
            "current_price": 8500.0,
        },
        {
            "ticker": "BMRI",
            "name": "Bank Mandiri",
            "sector": "Banking",
            "current_price": 6200.0,
        },
        {
            "ticker": "BBRI",
            "name": "Bank Rakyat Indonesia",
            "sector": "Banking",
            "current_price": 4800.0,
        },
        {
            "ticker": "TLKM",
            "name": "Telkom Indonesia",
            "sector": "Telecommunications",
            "current_price": 3200.0,
        },
        {
            "ticker": "ASII",
            "name": "Astra International",
            "sector": "Automotive",
            "current_price": 5500.0,
        },
    ]
