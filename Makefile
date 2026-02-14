dev:
	uv run uvicorn app.main:app --reload

format:
	uv run ruff format .

lint:
	uv run ruff check .

test:
	uv run pytest -v

test-cov:
	uv run pytest --cov=app --cov-report=html --cov-report=term

test-unit:
	uv run pytest -v -m unit

test-integration:
	uv run pytest -v -m integration

ci:
	uv run ruff format --check .
	uv run ruff check .
	uv run pytest -v
