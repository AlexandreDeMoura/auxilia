.PHONY: run migrate dev

migrate:
	uv run alembic upgrade head

run: migrate
	uv run uvicorn app.main:app --reload

dev: migrate
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload