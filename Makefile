.PHONY: install lockcheck test lint formatcheck typecheck diffcheck check

install:
	uv sync --locked --dev

lockcheck:
	uv lock --check

test:
	uv run --locked pytest

lint:
	uv run --locked ruff check .

formatcheck:
	uv run --locked ruff format --check .

typecheck:
	uv run --locked mypy src tests/typecheck

diffcheck:
	git diff --check

check: lockcheck test lint formatcheck typecheck diffcheck
