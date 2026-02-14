# Testing Guide

## Overview

This project now has a comprehensive test suite with **55 passing tests** covering all major functionality.

## Quick Start

```bash
# Install dependencies (including test dependencies)
uv sync

# Run all tests
make test

# Run tests with coverage report
make test-cov
```

## Test Coverage Summary

### ✅ 55 Tests Passing

#### Authentication Tests (7 tests)
- Login success/failure scenarios
- Invalid credentials handling
- Request validation

#### Stock CRUD Tests (26 tests)
- **Create**: Valid stocks, duplicate detection, case-insensitivity
- **Read**: Pagination, filtering by sector, empty/populated states
- **Update**: Partial updates, duplicate ticker prevention
- **Delete**: Success cases, not found handling

#### Utility Function Tests (18 tests)
- Ticker normalization
- Stock existence checking
- Pagination calculations
- 404 error handling

#### Application Tests (4 tests)
- App initialization
- API documentation endpoints
- OpenAPI schema validation

## Available Test Commands

| Command | Description |
|---------|-------------|
| `make test` | Run all tests |
| `make test-cov` | Run tests with coverage report (HTML) |
| `make test-unit` | Run only unit tests |
| `make test-integration` | Run only integration tests |
| `make ci` | Run all CI checks (format, lint, test) |

## Test Categories

### Unit Tests
Fast, isolated tests for individual functions:
- `test_utils.py` - Helper functions
- `test_main.py` - App setup
- Parts of `test_auth.py`

### Integration Tests
End-to-end API tests with database:
- `test_stocks.py` - Full CRUD operations
- Database integration scenarios

## Test Infrastructure

### Fixtures (in `conftest.py`)
- **`session`** - In-memory SQLite database per test
- **`client`** - FastAPI TestClient with DB override
- **`sample_stock_data`** - Sample stock for testing
- **`sample_stocks_list`** - Multiple stocks for pagination/filtering

### Configuration (`pytest.ini`)
- Verbose output by default
- Custom markers for unit/integration/slow tests
- Short traceback format

## CI/CD Integration

Tests automatically run on:
- ✅ Every push to master
- ✅ Every pull request
- ✅ Before deployment

GitHub Actions workflow ensures:
1. Code is formatted correctly (ruff format)
2. Code passes linting (ruff check)
3. All tests pass (pytest)
4. Only then: Deploy to VPS

## Coverage Report

Generate detailed HTML coverage report:

```bash
make test-cov
```

Then open `htmlcov/index.html` in your browser to see:
- Line-by-line coverage
- Missing coverage highlights
- Coverage percentage per module

## Writing New Tests

See [tests/README.md](tests/README.md) for:
- Test naming conventions
- Best practices
- How to use fixtures
- Example test patterns

## Troubleshooting

**Tests fail locally?**
- Run `uv sync` to install dependencies
- Check database migrations are up to date

**Tests pass locally but fail in CI?**
- Ensure no hardcoded file paths
- Verify all dependencies in `pyproject.toml`
- Check environment variables aren't required

**Need to debug a test?**
```bash
# Run single test with full output
uv run pytest tests/test_stocks.py::TestCreateStock::test_create_stock_success -vv -s
```

## Next Steps

1. **Run tests locally**: `make test`
2. **Check coverage**: `make test-cov` and review `htmlcov/index.html`
3. **Push to GitHub**: Tests will run automatically in CI
4. **Monitor CI**: Check GitHub Actions tab for results
