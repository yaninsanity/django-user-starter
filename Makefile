.PHONY: help install install-dev clean lint format test build upload-test upload check-version pre-commit-install pre-commit-run

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

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Code quality
lint:
	flake8 django_user_starter/
	isort --check-only django_user_starter/
	black --check django_user_starter/

format:
	isort django_user_starter/
	black django_user_starter/

# Testing
test:
	pytest

# Build and upload
build:
	python -m build

upload-test:
	twine upload --repository testpypi dist/*

upload:
	twine upload dist/*

# Version management
check-version:
	@echo "Current version: $$(python -c 'from django_user_starter import __version__; print(__version__)')"

# Pre-commit hooks
pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run --all-files
