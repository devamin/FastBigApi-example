install:
	poetry install

test:
	poetry shell
	pytest

run:
	poetry shell
	uvicorn hrflow.web.app:main_app  --port 8989 --factory