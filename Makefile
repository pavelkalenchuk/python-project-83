install:
		poetry install

dev:
		poetry run flask --app page_analyzer:app --debug run

lint_py:
		poetry run flake8 page_analyzer

lint_sql:
		poetry run sqlfluff lint database.sql --dialect postgres

lint: lint_py lint_sql

black:
		poetry run black page_analyzer

test:
		poetry run pytest -vv

test-coverage:
		poetry run pytest --cov=page_analyzer --cov-report xml

selfcheck:
		poetry check

check: selfcheck test lint

cov:
		poetry run pytest --cov=page_analyzer

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

database:
		psql -a -d $(DATABASE_URL) -f database.sql

build: install database