.DEFAULT_GOAL := help
SHELL=/bin/bash
ESCAPE = 
RUN=uv run

###### Development

install: install-uv ## Create venv and install dependencies
	uv venv
	uv sync

install-uv: ## Install the latest uv package
	pip install -U uv

install-dev: install ## Install development dependencies
	$(RUN) pip install -e .

test: test-static test-unit ## Run tests

test-unit: ## Run unit tests
	$(RUN) pytest

test-static: test-lint ## Run static tests

test-lint: ## Run linting
	$(RUN) ruff check .

format: ## Format code
	$(RUN) ruff check . --fix

###### Release

build: ## Build package with running test
	find . -type d -name "dist" -exec rm -rf {} +
	uv build

publish: build ## Publish package
	uv publish

###### Additional Commands

clean: ## Clean up cache and temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +

help: ## Print this help
	@grep -E '^([a-zA-Z_-]+:.*?## .*|######* .+)$$' Makefile \
		| sed 's/######* \(.*\)/@               $(ESCAPE)[1;31m\1$(ESCAPE)[0m/g' | tr '@' '\n' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'
