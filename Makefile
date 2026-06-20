.PHONY: install install-dev lint typecheck test clean generate run help

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  install       Install production dependencies"
	@echo "  install-dev   Install dev dependencies (includes dev, api)"
	@echo "  lint          Run ruff linter"
	@echo "  typecheck     Run mypy type checker"
	@echo "  test          Run pytest suite"
	@echo "  precommit     Install pre-commit hooks"
	@echo "  generate      Generate sample data"
	@echo "  run           Run ranking pipeline with sample JD"
	@echo "  clean         Remove build artifacts and cache"
	@echo "  docker-build  Build Docker image"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev,api]"

lint:
	ruff check src/candidate_ranker/

typecheck:
	mypy src/candidate_ranker/

test:
	pytest tests/ -v --cov=src/candidate_ranker --cov-report=term-missing

precommit:
	pre-commit install

generate:
	python -m candidate_ranker.io.generator

run:
	python -m candidate_ranker --help

clean:
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/ .coverage coverage.xml

docker-build:
	docker build -t candidate-ranker -f docker/Dockerfile .
