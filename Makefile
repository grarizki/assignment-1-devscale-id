dev:
	uv run uvicorn app.main:app --reload

format:
	uv run ruff format .

