.PHONY: install test lint typecheck check

install:
	uv sync --dev

test:
	uv run pytest

lint:
	uv run ruff check .

typecheck:
	uv run mypy src

check: lint typecheck test
