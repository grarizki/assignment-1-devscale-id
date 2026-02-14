"""
Tests for authentication endpoints
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
class TestLoginEndpoint:
    """Test cases for the /login endpoint"""

    def test_login_success(self, client: TestClient):
        """Test successful login with valid credentials"""
        response = client.post(
            "/login", json={"email": "admin@admin.com", "password": "admin123"}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Good!"}

    def test_login_invalid_email(self, client: TestClient):
        """Test login with invalid email"""
        response = client.post(
            "/login", json={"email": "wrong@email.com", "password": "admin123"}
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Email not found"

    def test_login_invalid_password(self, client: TestClient):
        """Test login with invalid password"""
        response = client.post(
            "/login", json={"email": "admin@admin.com", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid Password"

    def test_login_missing_email(self, client: TestClient):
        """Test login with missing email field"""
        response = client.post("/login", json={"password": "admin123"})
        assert response.status_code == 422  # Validation error

    def test_login_missing_password(self, client: TestClient):
        """Test login with missing password field"""
        response = client.post("/login", json={"email": "admin@admin.com"})
        assert response.status_code == 422  # Validation error

    def test_login_empty_body(self, client: TestClient):
        """Test login with empty request body"""
        response = client.post("/login", json={})
        assert response.status_code == 422  # Validation error

    def test_login_invalid_json(self, client: TestClient):
        """Test login with invalid JSON format"""
        response = client.post(
            "/login", data="not a json", headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
