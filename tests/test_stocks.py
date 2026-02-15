"""
Tests for stocks CRUD endpoints
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestCreateStock:
    """Test cases for POST /stocks/"""

    def test_create_stock_success(self, client: TestClient, sample_stock_data):
        """Test creating a new stock with valid data"""
        response = client.post("/stocks/", json=sample_stock_data)
        assert response.status_code == 201
        data = response.json()
        assert data["ticker"] == sample_stock_data["ticker"]
        assert data["name"] == sample_stock_data["name"]
        assert data["sector"] == sample_stock_data["sector"]
        assert data["current_price"] == sample_stock_data["current_price"]
        assert "id" in data

    def test_create_stock_duplicate_ticker(self, client: TestClient, sample_stock_data):
        """Test creating a stock with duplicate ticker fails"""
        # Create first stock
        client.post("/stocks/", json=sample_stock_data)
        # Try to create duplicate
        response = client.post("/stocks/", json=sample_stock_data)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_create_stock_ticker_case_insensitive(
        self, client: TestClient, sample_stock_data
    ):
        """Test that ticker symbols are case-insensitive"""
        client.post("/stocks/", json=sample_stock_data)
        # Try with lowercase ticker
        lowercase_data = {**sample_stock_data, "ticker": "bbca"}
        response = client.post("/stocks/", json=lowercase_data)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_create_stock_minimal_fields(self, client: TestClient):
        """Test creating stock with only required fields"""
        minimal_data = {"ticker": "TEST", "name": "Test Company"}
        response = client.post("/stocks/", json=minimal_data)
        assert response.status_code == 201
        data = response.json()
        assert data["ticker"] == "TEST"
        assert data["name"] == "Test Company"

    def test_create_stock_invalid_price(self, client: TestClient, sample_stock_data):
        """Test creating stock with invalid (negative) price"""
        invalid_data = {**sample_stock_data, "current_price": -100}
        response = client.post("/stocks/", json=invalid_data)
        assert response.status_code == 422  # Validation error


@pytest.mark.integration
class TestGetStocks:
    """Test cases for GET /stocks/"""

    def test_get_stocks_empty_list(self, client: TestClient):
        """Test getting stocks when database is empty"""
        response = client.get("/stocks/")
        assert response.status_code == 200
        data = response.json()
        assert data["stocks"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["page_size"] == 10

    def test_get_stocks_with_data(self, client: TestClient, sample_stocks_list):
        """Test getting stocks with data in database"""
        # Create multiple stocks
        for stock in sample_stocks_list:
            client.post("/stocks/", json=stock)

        response = client.get("/stocks/")
        assert response.status_code == 200
        data = response.json()
        assert len(data["stocks"]) == 5
        assert data["total"] == 5
        assert data["page"] == 1
        assert data["page_size"] == 10

    def test_get_stocks_pagination(self, client: TestClient, sample_stocks_list):
        """Test pagination works correctly"""
        # Create stocks
        for stock in sample_stocks_list:
            client.post("/stocks/", json=stock)

        # Get page 1 with 2 items per page
        response = client.get("/stocks/?page=1&page_size=2")
        data = response.json()
        assert len(data["stocks"]) == 2
        assert data["total"] == 5
        assert data["page"] == 1
        assert data["page_size"] == 2

        # Get page 2
        response = client.get("/stocks/?page=2&page_size=2")
        data = response.json()
        assert len(data["stocks"]) == 2
        assert data["page"] == 2

    def test_get_stocks_filter_by_sector(self, client: TestClient, sample_stocks_list):
        """Test filtering stocks by sector"""
        # Create stocks
        for stock in sample_stocks_list:
            client.post("/stocks/", json=stock)

        # Filter by Banking sector
        response = client.get("/stocks/?sector=Banking")
        data = response.json()
        assert len(data["stocks"]) == 3
        assert all(stock["sector"] == "Banking" for stock in data["stocks"])

        # Filter by Telecommunications sector
        response = client.get("/stocks/?sector=Telecommunications")
        data = response.json()
        assert len(data["stocks"]) == 1
        assert data["stocks"][0]["ticker"] == "TLKM"

    def test_get_stocks_invalid_page(self, client: TestClient):
        """Test getting stocks with invalid page number"""
        response = client.get("/stocks/?page=0")
        assert response.status_code == 422

    def test_get_stocks_large_page_size(self, client: TestClient):
        """Test page size limit enforcement"""
        response = client.get("/stocks/?page_size=1000")
        assert response.status_code == 422  # Should exceed max limit


@pytest.mark.integration
class TestGetStockByTicker:
    """Test cases for GET /stocks/{ticker}"""

    def test_get_stock_success(self, client: TestClient, sample_stock_data):
        """Test getting a specific stock by ticker"""
        # Create stock
        create_response = client.post("/stocks/", json=sample_stock_data)
        created_stock = create_response.json()

        # Get stock by ticker
        response = client.get(f"/stocks/{sample_stock_data['ticker']}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_stock["id"]
        assert data["ticker"] == sample_stock_data["ticker"]

    def test_get_stock_not_found(self, client: TestClient):
        """Test getting non-existent stock returns 404"""
        response = client.get("/stocks/NOTEXIST")
        assert response.status_code == 404

    def test_get_stock_case_insensitive(self, client: TestClient, sample_stock_data):
        """Test that ticker lookup is case-insensitive"""
        client.post("/stocks/", json=sample_stock_data)
        # Try with lowercase
        response = client.get("/stocks/bbca")
        assert response.status_code == 200
        assert response.json()["ticker"] == "BBCA"


@pytest.mark.integration
class TestUpdateStock:
    """Test cases for PATCH /stocks/{ticker}"""

    def test_update_stock_name(self, client: TestClient, sample_stock_data):
        """Test updating stock name"""
        client.post("/stocks/", json=sample_stock_data)
        update_data = {"name": "Bank Central Asia Tbk"}
        response = client.patch(
            f"/stocks/{sample_stock_data['ticker']}", json=update_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Bank Central Asia Tbk"
        assert data["ticker"] == sample_stock_data["ticker"]  # Unchanged

    def test_update_stock_price(self, client: TestClient, sample_stock_data):
        """Test updating stock price"""
        client.post("/stocks/", json=sample_stock_data)
        update_data = {"current_price": 9000.0}
        response = client.patch(
            f"/stocks/{sample_stock_data['ticker']}", json=update_data
        )
        assert response.status_code == 200
        assert response.json()["current_price"] == 9000.0

    def test_update_stock_ticker(self, client: TestClient, sample_stock_data):
        """Test updating stock ticker"""
        client.post("/stocks/", json=sample_stock_data)
        update_data = {"ticker": "BBCA2"}
        response = client.patch(
            f"/stocks/{sample_stock_data['ticker']}", json=update_data
        )
        assert response.status_code == 200
        assert response.json()["ticker"] == "BBCA2"

    def test_update_stock_duplicate_ticker(
        self, client: TestClient, sample_stocks_list
    ):
        """Test updating ticker to an existing one fails"""
        # Create two stocks
        client.post("/stocks/", json=sample_stocks_list[0])  # BBCA
        client.post("/stocks/", json=sample_stocks_list[1])  # BMRI

        # Try to update BMRI ticker to BBCA
        update_data = {"ticker": "BBCA"}
        response = client.patch("/stocks/BMRI", json=update_data)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_update_stock_not_found(self, client: TestClient):
        """Test updating non-existent stock returns 404"""
        response = client.patch("/stocks/NOTEXIST", json={"name": "Test"})
        assert response.status_code == 404

    def test_update_stock_partial(self, client: TestClient, sample_stock_data):
        """Test partial update only changes specified fields"""
        client.post("/stocks/", json=sample_stock_data)
        original_name = sample_stock_data["name"]

        # Update only price
        update_data = {"current_price": 10000.0}
        response = client.patch(
            f"/stocks/{sample_stock_data['ticker']}", json=update_data
        )
        data = response.json()
        assert data["current_price"] == 10000.0
        assert data["name"] == original_name  # Should remain unchanged


@pytest.mark.integration
class TestDeleteStock:
    """Test cases for DELETE /stocks/{ticker}"""

    def test_delete_stock_success(self, client: TestClient, sample_stock_data):
        """Test deleting a stock"""
        client.post("/stocks/", json=sample_stock_data)
        response = client.delete(f"/stocks/{sample_stock_data['ticker']}")
        assert response.status_code == 204

        # Verify stock is deleted
        get_response = client.get(f"/stocks/{sample_stock_data['ticker']}")
        assert get_response.status_code == 404

    def test_delete_stock_not_found(self, client: TestClient):
        """Test deleting non-existent stock returns 404"""
        response = client.delete("/stocks/NOTEXIST")
        assert response.status_code == 404

    def test_delete_stock_case_insensitive(self, client: TestClient, sample_stock_data):
        """Test delete works with case-insensitive ticker"""
        client.post("/stocks/", json=sample_stock_data)
        # Delete with lowercase ticker
        response = client.delete("/stocks/bbca")
        assert response.status_code == 204
