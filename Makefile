.PHONY: help install install-dev test test-cov lint format type-check clean docs run run-api

# Note: Make is not available on Windows by default.
# Windows users should use: 
#   PowerShell:  .\setup-windows.ps1 -Task <task>
#   Command Prompt: setup-windows.bat <task>
# Available tasks below work the same way on both systems.

help:  ## Show this help message
	@echo "Autonomous QA Platform - Development Tasks"
	@echo "=========================================="
	@echo "Note: Windows users should use setup-windows.ps1 or setup-windows.bat instead"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install project dependencies
	pip install --upgrade pip
	pip install -r requirements.txt
	playwright install

install-dev:  ## Install development dependencies
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	playwright install
	pre-commit install

test:  ## Run tests
	pytest tests/ -v

test-cov:  ## Run tests with coverage report
	pytest tests/ -v --cov=agents,tools,orchestration --cov-report=html --cov-report=term

lint:  ## Run linting checks
	flake8 agents/ tools/ orchestration/ api/ evaluation/
	pylint agents/ tools/ orchestration/ api/ evaluation/

format:  ## Format code with black and isort
	black agents/ tools/ orchestration/ api/ evaluation/ examples/
	isort agents/ tools/ orchestration/ api/ evaluation/ examples/

type-check:  ## Run type checking with mypy
	mypy agents/ tools/ orchestration/ api/ evaluation/

check: lint type-check test  ## Run all quality checks

clean:  ## Clean up Python cache files and directories
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/

docs:  ## Generate documentation
	cd docs && make html
	@echo "Documentation generated in docs/_build/html/"

run:  ## Run basic workflow example
	python examples/basic_workflow.py

run-api:  ## Start FastAPI development server
	uvicorn examples.fastapi_server:app --reload --host 0.0.0.0 --port 8000

serve-docs:  ## Serve documentation
	mkdocs serve

setup:  ## Complete setup (install + create directories)
	@echo "Setting up Autonomous QA Platform..."
	$(MAKE) install-dev
	mkdir -p logs data/chromadb data/persist
	cp .env.example .env
	@echo "✓ Setup complete! Next: Edit .env with your OpenAI API key"

test-api:  ## Test API endpoints
	curl -X GET http://localhost:8000/api/health
	@echo "\nAPI is running!"

shell:  ## Open Python shell with project context
	python -i -c "from orchestration.agent_workflow import AutonomousQAWorkflow; workflow = AutonomousQAWorkflow()"

venv-activate:  ## Show virtual environment activation command
	@echo "macOS/Linux: source venv/bin/activate"
	@echo "Windows: venv\\Scripts\\activate"

requirements-update:  ## Update all dependencies to latest versions
	pip list --outdated
	pip install --upgrade pip setuptools wheel
	pip install --upgrade -r requirements.txt
	pip list

update-playwright:  ## Update Playwright browsers
	playwright install --with-deps

pre-commit-run:  ## Run pre-commit hooks on all files
	pre-commit run --all-files

all: clean install-dev test  ## Full setup and test