"""
Tests for utility functions
"""

import pytest
from sqlmodel import Session
from fastapi import HTTPException
from app.utils.stock_helpers import (
    normalize_ticker,
    get_stock_or_404,
    check_ticker_exists,
)
from app.utils.pagination import PaginationParams
from app.models.database import Stocks


@pytest.mark.unit
class TestNormalizeTicker:
    """Test cases for normalize_ticker function"""

    def test_normalize_lowercase(self):
        """Test normalizing lowercase ticker to uppercase"""
        assert normalize_ticker("bbca") == "BBCA"

    def test_normalize_mixed_case(self):
        """Test normalizing mixed case ticker"""
        assert normalize_ticker("BbCa") == "BBCA"

    def test_normalize_already_uppercase(self):
        """Test normalizing already uppercase ticker"""
        assert normalize_ticker("BBCA") == "BBCA"

    def test_normalize_with_whitespace(self):
        """Test normalizing ticker with whitespace"""
        assert normalize_ticker("  bbca  ") == "BBCA"
        assert normalize_ticker("bb ca") == "BB CA"

    def test_normalize_empty_string(self):
        """Test normalizing empty string"""
        assert normalize_ticker("") == ""

    def test_normalize_with_numbers(self):
        """Test normalizing ticker with numbers"""
        assert normalize_ticker("test123") == "TEST123"


@pytest.mark.unit
class TestCheckTickerExists:
    """Test cases for check_ticker_exists function"""

    def test_ticker_exists(self, session: Session):
        """Test checking if ticker exists returns True"""
        # Create a stock
        stock = Stocks(ticker="BBCA", name="Bank Central Asia")
        session.add(stock)
        session.commit()

        assert check_ticker_exists(session, "BBCA") is True

    def test_ticker_exists_case_insensitive(self, session: Session):
        """Test ticker existence check is case-insensitive"""
        stock = Stocks(ticker="BBCA", name="Bank Central Asia")
        session.add(stock)
        session.commit()

        assert check_ticker_exists(session, "bbca") is True
        assert check_ticker_exists(session, "BbCa") is True

    def test_ticker_not_exists(self, session: Session):
        """Test checking non-existent ticker returns False"""
        assert check_ticker_exists(session, "NOTEXIST") is False

    def test_ticker_not_exists_empty_db(self, session: Session):
        """Test checking ticker in empty database"""
        assert check_ticker_exists(session, "BBCA") is False


@pytest.mark.unit
class TestGetStockOr404:
    """Test cases for get_stock_or_404 function"""

    def test_get_stock_success(self, session: Session):
        """Test successfully getting a stock"""
        stock = Stocks(ticker="BBCA", name="Bank Central Asia", current_price=8500.0)
        session.add(stock)
        session.commit()

        result = get_stock_or_404(session, "BBCA")
        assert result.ticker == "BBCA"
        assert result.name == "Bank Central Asia"
        assert result.current_price == 8500.0

    def test_get_stock_case_insensitive(self, session: Session):
        """Test getting stock with case-insensitive ticker"""
        stock = Stocks(ticker="BBCA", name="Bank Central Asia")
        session.add(stock)
        session.commit()

        result = get_stock_or_404(session, "bbca")
        assert result.ticker == "BBCA"

    def test_get_stock_not_found_raises_404(self, session: Session):
        """Test that non-existent stock raises 404 HTTPException"""
        with pytest.raises(HTTPException) as exc_info:
            get_stock_or_404(session, "NOTEXIST")

        assert exc_info.value.status_code == 404
        assert "not found" in exc_info.value.detail

    def test_get_stock_with_whitespace(self, session: Session):
        """Test getting stock with whitespace in ticker"""
        stock = Stocks(ticker="BBCA", name="Bank Central Asia")
        session.add(stock)
        session.commit()

        result = get_stock_or_404(session, "  bbca  ")
        assert result.ticker == "BBCA"


@pytest.mark.unit
class TestPaginationParams:
    """Test cases for PaginationParams"""

    def test_default_values(self):
        """Test default pagination parameters"""
        params = PaginationParams()
        assert params.page == 1
        assert params.page_size == 10

    def test_custom_values(self):
        """Test custom pagination parameters"""
        params = PaginationParams(page=2, page_size=20)
        assert params.page == 2
        assert params.page_size == 20

    def test_calculate_offset_first_page(self):
        """Test offset calculation for first page"""
        params = PaginationParams(page=1, page_size=10)
        assert params.calculate_offset() == 0

    def test_calculate_offset_second_page(self):
        """Test offset calculation for second page"""
        params = PaginationParams(page=2, page_size=10)
        assert params.calculate_offset() == 10

    def test_calculate_offset_third_page(self):
        """Test offset calculation for third page"""
        params = PaginationParams(page=3, page_size=20)
        assert params.calculate_offset() == 40

    def test_invalid_page_number(self):
        """Test that page number must be at least 1"""
        with pytest.raises(Exception):  # Pydantic validation error
            PaginationParams(page=0, page_size=10)

    def test_invalid_page_size(self):
        """Test that page size has limits"""
        with pytest.raises(Exception):  # Pydantic validation error
            PaginationParams(page=1, page_size=0)

        with pytest.raises(Exception):  # Pydantic validation error
            PaginationParams(page=1, page_size=101)  # Exceeds max limit
