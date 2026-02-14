# Test Suite Documentation

This directory contains comprehensive tests for the FastAPI application.

## Test Structure

```
tests/
├── __init__.py          # Test package initialization
├── conftest.py          # Pytest fixtures and configuration
├── test_auth.py         # Authentication endpoint tests
├── test_stocks.py       # Stock CRUD endpoint tests
├── test_utils.py        # Utility function tests
└── test_main.py         # Main application tests
```

## Running Tests

### Run all tests
```bash
make test
# or
uv run pytest -v
```

### Run tests with coverage
```bash
make test-cov
# Generates HTML coverage report in htmlcov/index.html
```

### Run only unit tests
```bash
make test-unit
# or
uv run pytest -v -m unit
```

### Run only integration tests
```bash
make test-integration
# or
uv run pytest -v -m integration
```

### Run specific test file
```bash
uv run pytest tests/test_stocks.py -v
```

### Run specific test class
```bash
uv run pytest tests/test_stocks.py::TestCreateStock -v
```

### Run specific test function
```bash
uv run pytest tests/test_stocks.py::TestCreateStock::test_create_stock_success -v
```

## Test Categories

### Unit Tests
Marked with `@pytest.mark.unit`
- Test individual functions and utilities in isolation
- Fast execution
- No external dependencies

Examples:
- `test_utils.py` - Tests for helper functions
- `test_main.py` - Basic app initialization tests
- `test_auth.py` - Simple authentication logic tests

### Integration Tests
Marked with `@pytest.mark.integration`
- Test complete request/response cycles
- Use in-memory SQLite database
- Test full API endpoints

Examples:
- `test_stocks.py` - Full CRUD operations testing
- Database integration tests

## Test Coverage

Current test coverage includes:

### Authentication (`test_auth.py`)
- ✅ Successful login
- ✅ Invalid email handling
- ✅ Invalid password handling
- ✅ Missing field validation
- ✅ Invalid JSON handling

### Stocks CRUD (`test_stocks.py`)
- ✅ Create stock (valid, duplicate, case-insensitive)
- ✅ Get stocks (empty, with data, pagination, filtering)
- ✅ Get single stock (success, not found, case-insensitive)
- ✅ Update stock (partial, full, duplicate ticker)
- ✅ Delete stock (success, not found)

### Utilities (`test_utils.py`)
- ✅ Ticker normalization
- ✅ Ticker existence checking
- ✅ Stock retrieval with 404 handling
- ✅ Pagination parameter validation

## Test Fixtures

Key fixtures available in `conftest.py`:

### `session`
In-memory SQLite database session for isolated testing.

```python
def test_example(session: Session):
    stock = Stocks(ticker="TEST", name="Test Stock")
    session.add(stock)
    session.commit()
```

### `client`
FastAPI TestClient with database dependency override.

```python
def test_example(client: TestClient):
    response = client.get("/stocks/")
    assert response.status_code == 200
```

### `sample_stock_data`
Dictionary with sample stock data for testing.

```python
def test_example(sample_stock_data):
    # sample_stock_data = {"ticker": "BBCA", "name": "...", ...}
    pass
```

### `sample_stocks_list`
List of multiple sample stocks for pagination/filtering tests.

```python
def test_example(sample_stocks_list):
    # List of 5 stocks across different sectors
    pass
```

## Writing New Tests

### Test Naming Convention
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Example Test
```python
import pytest
from fastapi.testclient import TestClient

@pytest.mark.integration
class TestMyFeature:
    """Test cases for my feature"""

    def test_feature_works(self, client: TestClient):
        """Test that feature works correctly"""
        response = client.get("/my-endpoint")
        assert response.status_code == 200
        assert response.json()["status"] == "success"
```

### Best Practices
1. **Use descriptive test names** - Test names should describe what is being tested
2. **One assertion per concept** - Tests should verify one behavior
3. **Use fixtures** - Leverage existing fixtures for database and client setup
4. **Mark tests appropriately** - Use `@pytest.mark.unit` or `@pytest.mark.integration`
5. **Test edge cases** - Include tests for invalid input, empty data, etc.
6. **Clean test data** - Use fresh database session (automatic with fixtures)

## CI/CD Integration

Tests are automatically run in GitHub Actions on:
- Every push to master
- Every pull request

The CI pipeline requires all tests to pass before deployment.

## Troubleshooting

### Tests fail with database errors
Ensure you're using the `session` fixture which provides an isolated in-memory database.

### Import errors
Make sure you've run `uv sync` to install all dependencies including test dependencies.

### Coverage not generating
Install pytest-cov: `uv sync` (it's in dev dependencies)

### Tests pass locally but fail in CI
Check that:
- All test dependencies are in `pyproject.toml`
- Tests don't depend on local files or environment variables
- Database migrations are compatible with SQLite
