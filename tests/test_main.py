"""
Tests for main application setup
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
class TestMainApp:
    """Test cases for main application"""

    def test_app_exists(self, client: TestClient):
        """Test that the app is properly initialized"""
        assert client.app is not None

    def test_scalar_docs_endpoint(self, client: TestClient):
        """Test that Scalar API documentation endpoint exists"""
        response = client.get("/scalar")
        assert response.status_code == 200

    def test_openapi_schema(self, client: TestClient):
        """Test that OpenAPI schema is available"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema

    def test_health_check_endpoints_exist(self, client: TestClient):
        """Test that critical endpoints are registered"""
        response = client.get("/openapi.json")
        schema = response.json()
        paths = schema["paths"]

        # Check auth endpoints
        assert "/login" in paths

        # Check stocks endpoints
        assert "/stocks/" in paths
        assert "/stocks/{ticker}" in paths
