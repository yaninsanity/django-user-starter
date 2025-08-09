.PHONY: help install install-dev clean lint format test build upload-test upload check-version pre-commit-install pre-commit-run

# Python executable - can be overridden with: make PYTHON=/path/to/python
PYTHON ?= python

# Default target
help:
	@echo "Available commands:"
	@echo "  install           Install production dependencies"
	@echo "  install-dev       Install development dependencies"
	@echo "  clean             Clean build artifacts"
	@echo "  lint              Run code linting"
	@echo "  format            Format code with black and isort"
	@echo "  test              Run tests"
	@echo "  build             Build package"
	@echo "  upload-test       Upload to TestPyPI"
	@echo "  upload            Upload to PyPI"
	@echo "  check-version     Check current version"
	@echo "  pre-commit-install Install pre-commit hooks"
	@echo "  pre-commit-run    Run pre-commit on all files"
	@echo ""
	@echo "Note: Use PYTHON=/path/to/python to specify Python executable"
	@echo "Example: make lint PYTHON=.venv/bin/python"

# Installation
install:
	$(PYTHON) -m pip install -e .

install-dev:
	$(PYTHON) -m pip install -e ".[dev]"

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Code quality
lint:
	$(PYTHON) -m flake8 django_user_starter/ tests/
	$(PYTHON) -m isort --check-only django_user_starter/ tests/
	$(PYTHON) -m black --check django_user_starter/ tests/

format:
	$(PYTHON) -m isort django_user_starter/ tests/
	$(PYTHON) -m black django_user_starter/ tests/

# Testing
test:
	$(PYTHON) -m pytest tests/ --cov=django_user_starter --cov-report=term-missing

# Build and upload
build:
	$(PYTHON) -m build

upload-test:
	$(PYTHON) -m twine upload --repository testpypi dist/*

upload:
	$(PYTHON) -m twine upload dist/*

# Version management
check-version:
	@echo "Current version: $$($(PYTHON) -c 'from django_user_starter import __version__; print(__version__)')"

# Pre-commit hooks
pre-commit-install:
	$(PYTHON) -m pre_commit install

pre-commit-run:
	$(PYTHON) -m pre_commit run --all-files
