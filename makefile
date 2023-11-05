AME := hrflow
INSTALL_STAMP := .install.stamp
POETRY := $(shell command -v poetry 2> /dev/null)

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "  install     install packages and prepare environment"
	@echo "  test        run all the tests"
	@echo "  run        run uvicorn server"
	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."

install: $(INSTALL_STAMP)
$(INSTALL_STAMP): pyproject.toml poetry.lock
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) install
	touch $(INSTALL_STAMP)

.PHONY: test
test: $(INSTALL_STAMP)
	$(POETRY) run pytest -p no:warnings -v

.PHONY: run
run: $(INSTALL_STAMP)
	$(POETRY) run uvicorn hrflow.web.app:main_app  --port 8989 --factory 