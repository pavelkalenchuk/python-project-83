install:
		poetry install

dev:
		poetry run flask --app page_analyzer:app run

lint:
		poetry run flake8 page_analyzer

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