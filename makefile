VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
ALEMBIC := $(VENV)/bin/alembic
UVICORN := $(VENV)/bin/fastapi
PYTEST := $(VENV)/bin/pytest

venv:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

install: venv
	$(PIP) install -r requirements/dev.txt

run:
	docker-compose up --build

migrate_up:
	$(ALEMBIC) -c app/alembic.ini upgrade head

migrate:
	@read -p "Migration message: " msg; \
	$(ALEMBIC) -c app/alembic.ini revision --autogenerate -m "$$msg"

lint:
	ruff check app tests

format:
	ruff format app tests
	ruff check --fix app tests

typecheck:
	mypy app

test:
	@pytest \
		--cov=app \
		--cov-report=term-missing \
		--cov-report=xml \
		-v

check: lint typecheck test