# Stock Options API

A RESTful API for managing Indonesian stock market data built with FastAPI, SQLModel, and SQLite.

## Features

- **CRUD Operations** for stock data (Create, Read, Update, Delete)
- **Pagination Support** for listing stocks
- **Sector Filtering** to filter stocks by business sector
- **Ticker-based Operations** - All operations use stock ticker symbols as identifiers
- **Dependency Injection** for clean database session management
- **Pydantic Validation** for request/response schemas
- **Interactive API Documentation** with Scalar UI
- **Pre-seeded Data** with Indonesian stocks (BBCA, BMRI, BBRI, BUMI)

## Tech Stack

- **FastAPI** - Modern, fast web framework
- **SQLModel** - SQL databases with Python type annotations
- **Pydantic** - Data validation using Python type hints
- **SQLite** - Lightweight database
- **Uvicorn** - ASGI server
- **Scalar** - Beautiful API documentation UI

## Project Structure

```
assignment-1/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   └── settings.py          # Application settings
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py          # SQLModel database models
│   │   ├── engine.py            # Database engine & session
│   │   ├── init_db.py           # Database initialization script
│   │   └── seed_data.py         # Data seeding script
│   ├── router/
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication endpoints
│   │   └── stocks.py            # Stock endpoints
│   ├── schema/
│   │   ├── __init__.py
│   │   ├── auth.py              # Auth schemas
│   │   └── stocks.py            # Stock schemas (Pydantic)
│   ├── utils/
│   │   ├── __init__.py
│   │   └── query_params.py      # Query parameter utilities
│   ├── __init__.py
│   └── main.py                  # FastAPI application entry point
├── alembic/                     # Database migrations (optional)
├── config.py                    # Configuration file
├── database.db                  # SQLite database
├── Makefile                     # Development commands
├── pyproject.toml              # Project dependencies
├── uv.lock                     # Lock file for dependencies
└── README.md
```

## Installation

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip

### Setup

1. **Clone the repository**

```bash
git clone <repository-url>
cd assignment-1
```

2. **Install dependencies**

Using uv (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
```

3. **Initialize the database**

Using uv:
```bash
uv run python -m app.models.init_db
```

Or using python directly:
```bash
python -m app.models.init_db
```

4. **Seed dummy data (optional)**

Using uv:
```bash
uv run python -m app.models.seed_data
```

Or using python directly:
```bash
python -m app.models.seed_data
```

## Running the Application

### Development Mode

Using Makefile:
```bash
make dev
```

Or directly with uvicorn:
```bash
uvicorn app.main:app --reload
```

Or with uv:
```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:
- API Base URL: `http://localhost:8000`
- API Documentation (Scalar): `http://localhost:8000/docs`
- OpenAPI Schema: `http://localhost:8000/openapi.json`

## API Endpoints

### Stocks

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/stocks/` | Get paginated list of stocks |
| `POST` | `/stocks/` | Create a new stock |
| `GET` | `/stocks/{ticker}` | Get stock by ticker symbol |
| `PATCH` | `/stocks/{ticker}` | Update stock by ticker |
| `DELETE` | `/stocks/{ticker}` | Delete stock by ticker |
| `POST` | `/stocks/seed` | Seed database with dummy stocks |

### Query Parameters

**GET /stocks/**
- `page` (int, default: 1) - Page number
- `page_size` (int, default: 10) - Items per page
- `sector` (str, optional) - Filter by sector (e.g., "Banking", "Mining")

## API Usage Examples

### Get All Stocks (Paginated)

```bash
curl http://localhost:8000/stocks/?page=1&page_size=10
```

**Response:**
```json
{
  "stocks": [
    {
      "ticker": "BBCA",
      "name": "PT Bank Central Asia Tbk",
      "sector": "Banking",
      "current_price": 9800.0,
      "description": "Largest private bank in Indonesia by market capitalization",
      "id": "b66ab02a-7dc7-4e36-b346-89a4b44a68ab"
    }
  ],
  "total": 4,
  "page": 1,
  "page_size": 10
}
```

### Get Stock by Ticker

```bash
curl http://localhost:8000/stocks/BBCA
```

### Create a New Stock

```bash
curl -X POST http://localhost:8000/stocks/ \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "TLKM",
    "name": "PT Telkom Indonesia Tbk",
    "sector": "Telecommunication",
    "current_price": 3850.0,
    "description": "State-owned telecommunications company"
  }'
```

### Update Stock Price

```bash
curl -X PATCH http://localhost:8000/stocks/BBCA \
  -H "Content-Type: application/json" \
  -d '{
    "current_price": 10000.0
  }'
```

### Delete a Stock

```bash
curl -X DELETE http://localhost:8000/stocks/BUMI
```

### Filter Stocks by Sector

```bash
curl http://localhost:8000/stocks/?sector=Banking
```

### Seed Dummy Data

```bash
curl -X POST http://localhost:8000/stocks/seed
```

## Database Schema

### Stocks Table

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key (auto-generated) |
| `ticker` | String(10) | Stock ticker symbol (unique, indexed) |
| `name` | String | Full company name |
| `sector` | String(100) | Business sector (optional) |
| `current_price` | Float | Current stock price (optional) |
| `description` | String(1000) | Company description (optional) |

### Pre-seeded Stocks

| Ticker | Name | Sector | Price (IDR) |
|--------|------|--------|-------------|
| BBCA | PT Bank Central Asia Tbk | Banking | 9,800 |
| BMRI | PT Bank Mandiri (Persero) Tbk | Banking | 6,250 |
| BBRI | PT Bank Rakyat Indonesia (Persero) Tbk | Banking | 5,100 |
| BUMI | PT Bumi Resources Tbk | Mining | 142 |

## Data Models

### StockCreate (Request)

```python
{
  "ticker": "BBCA",                    # Required, 1-10 chars
  "name": "PT Bank Central Asia Tbk",  # Required, 1-255 chars
  "sector": "Banking",                 # Optional, max 100 chars
  "current_price": 9800.0,             # Optional, must be > 0
  "description": "Description here"    # Optional, max 1000 chars
}
```

### StockUpdate (Request)

All fields are optional. Only provided fields will be updated.

```python
{
  "ticker": "BBCA",          # Optional
  "name": "New Name",        # Optional
  "sector": "Banking",       # Optional
  "current_price": 10000.0,  # Optional
  "description": "Updated"   # Optional
}
```

### StockResponse

```python
{
  "id": "uuid-here",
  "ticker": "BBCA",
  "name": "PT Bank Central Asia Tbk",
  "sector": "Banking",
  "current_price": 9800.0,
  "description": "Largest private bank in Indonesia"
}
```

### StockList (Paginated Response)

```python
{
  "stocks": [StockResponse, ...],
  "total": 4,
  "page": 1,
  "page_size": 10
}
```

## Development

### Database Management

**Create tables:**
```bash
uv run python -m app.models.init_db
# or: python -m app.models.init_db
```

**Seed data:**
```bash
uv run python -m app.models.seed_data
# or: python -m app.models.seed_data
```

**Reset database:**
```bash
rm database.db
uv run python -m app.models.init_db
uv run python -m app.models.seed_data
```

### Running Tests

```bash
pytest
```

## Configuration

Environment variables can be set in a `.env` file:

```env
DATABASE_URL=sqlite:///./database.db
APP_NAME=stockOptions
VERSION=0.0.1
```

## Key Features Explained

### Dependency Injection

The API uses FastAPI's dependency injection for database sessions:

```python
@stocks_router.get("/{ticker}")
async def get_stock(ticker: str, session: Session = Depends(get_db)):
    # session is automatically provided and managed
    stock = session.exec(select(Stocks).where(Stocks.ticker == ticker)).first()
    return stock
```

### Ticker-based Operations

All CRUD operations use stock ticker symbols as identifiers instead of UUIDs, making the API more intuitive:

- ✅ `GET /stocks/BBCA` - Clear and readable
- ❌ `GET /stocks/b66ab02a-7dc7-4e36-b346-89a4b44a68ab` - Complex and hard to remember

### Automatic Validation

Pydantic schemas provide automatic validation:

```python
class StockCreate(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=10)
    current_price: Optional[float] = Field(None, gt=0)  # Must be > 0
```

## API Documentation

Once the server is running, visit:

- **Scalar UI**: `http://localhost:8000/docs` - Beautiful, interactive API documentation
- **OpenAPI JSON**: `http://localhost:8000/openapi.json` - Machine-readable API specification

## Error Handling

The API returns standard HTTP status codes:

- `200 OK` - Successful GET/PATCH requests
- `201 Created` - Successful POST requests
- `204 No Content` - Successful DELETE requests
- `400 Bad Request` - Invalid input or duplicate ticker
- `404 Not Found` - Stock not found
- `422 Unprocessable Entity` - Validation errors
- `500 Internal Server Error` - Server errors

**Example error response:**
```json
{
  "detail": "Stock with ticker BBCA already exists"
}
```

## Database Migrations with Alembic

This project uses Alembic for database schema versioning. Here's everything you need to know:

### Using Alembic

**Create a new migration after changing models:**
```bash
uv run alembic revision --autogenerate -m "description of change"
```

**Apply migrations:**
```bash
uv run alembic upgrade head
```

**Check current migration status:**
```bash
uv run alembic current
```

**View migration history:**
```bash
uv run alembic history
```

**Rollback one migration:**
```bash
uv run alembic downgrade -1
```

### Common Migration Issues and Solutions

#### Issue 1: "Cannot add a NOT NULL column with default value NULL"

**Error:**
```
sqlite3.OperationalError: Cannot add a NOT NULL column with default value NULL
```

**Cause:** Adding a required field to an existing table without specifying a default value for existing rows.

**Solution:** Manually add `server_default` to the migration:

```python
# Generated migration (will fail):
op.add_column('stocks', sa.Column('new_field', sa.VARCHAR(), nullable=False))

# Fixed migration:
op.add_column('stocks', sa.Column('new_field', sa.VARCHAR(),
    nullable=False, server_default='default value'))
```

**Prevention:** Always make new fields optional initially:
```python
# In your model
new_field: Optional[str] = Field(default=None)
```

#### Issue 2: "ALTER COLUMN syntax error" with SQLite

**Error:**
```
sqlite3.OperationalError: near "ALTER": syntax error
[SQL: ALTER TABLE stocks ALTER COLUMN "field" DROP NOT NULL]
```

**Cause:** SQLite has limited `ALTER COLUMN` support. It cannot:
- Change column types
- Change NULL/NOT NULL constraints
- Add/remove defaults on existing columns

**Solution:** Use batch mode operations. The migration should be wrapped in `batch_alter_table`:

```python
# Generated migration (will fail with SQLite):
def upgrade():
    op.alter_column('stocks', 'field_name', nullable=True)

# Fixed migration for SQLite:
def upgrade():
    with op.batch_alter_table('stocks', schema=None) as batch_op:
        batch_op.alter_column('field_name', nullable=True)
```

**Our Configuration:** The `alembic/env.py` is already configured with `render_as_batch=True` for automatic batch mode support.

#### Issue 3: "Target database is not up to date"

**Error:**
```
ERROR [alembic.util.messaging] Target database is not up to date.
```

**Cause:** You're trying to create a migration when there are pending migrations.

**Solution:** Apply pending migrations first:
```bash
uv run alembic upgrade head
```

Then create your new migration:
```bash
uv run alembic revision --autogenerate -m "your change"
```

### Best Practices for Database Changes

#### 1. Always Review Auto-Generated Migrations

After running `alembic revision --autogenerate`, **always check** the generated file in `alembic/versions/`:

```bash
# Generate migration
uv run alembic revision --autogenerate -m "add field"

# Review the file
cat alembic/versions/XXXXX_add_field.py

# Make manual adjustments if needed
# Then apply
uv run alembic upgrade head
```

#### 2. Make New Fields Optional

```python
# ✅ Good - Easy to migrate
new_field: Optional[str] = Field(default=None)

# ⚠️ Requires careful migration handling
new_field: str = Field(default="value")
```

#### 3. Two-Step Migration for Required Fields

If a field must be NOT NULL:

**Step 1:** Add as nullable with default
```python
# Migration 1
op.add_column('stocks', sa.Column('new_field', sa.VARCHAR(),
    nullable=True, server_default='default'))
```

**Step 2:** Populate data and make NOT NULL
```python
# Migration 2 (after data is populated)
with op.batch_alter_table('stocks', schema=None) as batch_op:
    batch_op.alter_column('new_field', nullable=False)
```

#### 4. Testing Migrations

Always test migrations on a fresh database:

```bash
# Backup current database
cp database.db database.db.backup

# Test fresh migration
rm database.db
uv run alembic upgrade head
uv run python -m app.models.seed_data

# If successful, restore or continue
# If failed, restore backup: mv database.db.backup database.db
```

### SQLite vs PostgreSQL/MySQL

**SQLite Limitations:**
- Limited ALTER TABLE support
- No concurrent writes
- Good for development, not recommended for production

**For Production:**
Consider using PostgreSQL or MySQL where Alembic migrations work without batch mode complications.

Update your `.env`:
```env
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/dbname

# MySQL
DATABASE_URL=mysql://user:password@localhost/dbname
```

### Migration Workflow Summary

```bash
# 1. Edit your model (app/models/database.py)

# 2. Generate migration
uv run alembic revision --autogenerate -m "description"

# 3. Review generated file in alembic/versions/

# 4. Fix any SQLite-specific issues:
#    - Add server_default for NOT NULL columns
#    - Wrap ALTER COLUMN in batch_alter_table

# 5. Apply migration
uv run alembic upgrade head

# 6. Verify
uv run alembic current
sqlite3 database.db "PRAGMA table_info(stocks);"
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Author

Created as part of DevScale Python AI assignment.

## Acknowledgments

- FastAPI for the amazing framework
- SQLModel for the elegant ORM
- Scalar for beautiful API documentation
