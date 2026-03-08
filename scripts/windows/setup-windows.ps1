#Requires -Version 5.0
# Autonomous QA Platform - Windows Setup Script
# Usage: .\setup-windows.ps1 -Task setup

param([string]$Task = 'setup')

# Utility functions
function Write-H { param([string]$s); Write-Host ""; Write-Host ("=" * 80) -Fore Cyan; Write-Host $s -Fore Green; Write-Host ("=" * 80) -Fore Cyan; Write-Host "" }
function Write-OK { param([string]$s); Write-Host "[OK] $s" -Fore Green }
function Write-ERR { param([string]$s); Write-Host "[ERROR] $s" -Fore Red }
function Write-I { param([string]$s); Write-Host "  $s" -Fore Yellow }

if ($Task -eq 'setup') {
    Write-H "Autonomous QA Platform - Complete Setup"
    Write-H "Installing Python Dependencies"
    Write-I "Upgrading pip..."
    python -m pip install --upgrade pip setuptools wheel
    if ($LASTEXITCODE -ne 0) { Write-ERR "Failed to upgrade pip"; exit 1 }
    Write-I "Installing core dependencies..."
    pip install -r requirements/requirements.txt
    if ($LASTEXITCODE -ne 0) { Write-ERR "Failed to install core dependencies"; exit 1 }
    Write-I "Installing dev dependencies..."
    pip install -r requirements/requirements-dev.txt
    if ($LASTEXITCODE -ne 0) { Write-ERR "Failed to install dev dependencies"; exit 1 }
    Write-OK "Dependencies installed"
    
    Write-H "Installing Playwright Browsers"
    Write-I "Installing Playwright browsers (this may take a few minutes)..."
    playwright install
    if ($LASTEXITCODE -ne 0) { Write-ERR "Failed to install Playwright browsers"; exit 1 }
    Write-OK "Playwright browsers installed"
    
    Write-H "Creating Required Directories"
    $dirs = @('logs', 'data/chromadb', 'data/persist', 'playwright-tests/tests/generated')
    foreach ($dir in $dirs) {
        if (-not (Test-Path $dir -PathType Container)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null; Write-OK "Created directory: $dir" }
        else { Write-I "Directory already exists: $dir" }
    }
    
    Write-H "Setting Up Environment"
    if (-not (Test-Path '.env' -PathType Leaf)) {
        if (Test-Path '.env.example' -PathType Leaf) { Copy-Item '.env.example' '.env'; Write-OK "Created .env file from .env.example" }
        else { Write-ERR "Error: .env.example not found"; exit 1 }
        Write-Host ""; Write-Host "IMPORTANT: Edit .env and add your OpenAI API key:" -Fore Yellow; Write-Host "   OPENAI_API_KEY=sk-..." -Fore Cyan; Write-Host ""
    } else { Write-I ".env file already exists" }
    
    Write-H "Setup Complete!"
    Write-Host "Next steps:" -Fore Green
    Write-Host "  1. Edit .env with your OpenAI API key" -Fore Cyan
    Write-Host "  2. Run tests: .\setup-windows.ps1 -Task test" -Fore Cyan  
    Write-Host "  3. Run API: .\setup-windows.ps1 -Task run-api" -Fore Cyan
    Write-Host ""
}
elseif ($Task -eq 'install') {
    Write-H "Installing Python Dependencies"
    Write-I "Upgrading pip..."
    python -m pip install --upgrade pip setuptools wheel
    if ($LASTEXITCODE -ne 0) { Write-ERR "Failed to upgrade pip"; exit 1 }
    Write-I "Installing core dependencies..."
    pip install -r requirements/requirements.txt
    if ($LASTEXITCODE -ne 0) { Write-ERR "Failed to install core dependencies"; exit 1 }
    Write-OK "Dependencies installed"
}
elseif ($Task -eq 'install-dev') {
    Write-H "Installing Development Dependencies"
    python -m pip install --upgrade pip setuptools wheel
    pip install -r requirements/requirements.txt
    pip install -r requirements/requirements-dev.txt
    Write-OK "Dev dependencies installed"
}
elseif ($Task -eq 'test') {
    Write-H "Running Tests"
    pytest tests/ -v
}
elseif ($Task -eq 'test-cov') {
    Write-H "Running Tests with Coverage"
    pytest tests/ -v --cov=agents,tools,orchestration --cov-report=html --cov-report=term
    Write-OK "Coverage report generated in htmlcov/index.html"
}
elseif ($Task -eq 'lint') {
    Write-H "Running Linting Checks"
    flake8 agents/ tools/ orchestration/ api/ evaluation/
    pylint agents/ tools/ orchestration/ api/ evaluation/
}
elseif ($Task -eq 'format') {
    Write-H "Formatting Code"
    black agents/ tools/ orchestration/ api/ evaluation/ examples/
    isort agents/ tools/ orchestration/ api/ evaluation/ examples/
    Write-OK "Code formatted"
}
elseif ($Task -eq 'type-check') {
    Write-H "Running Type Checking"
    mypy agents/ tools/ orchestration/ api/ evaluation/
}
elseif ($Task -eq 'check') {
    Write-H "Running All Quality Checks"
    Write-I "Running linting..."; flake8 agents/ tools/ orchestration/ api/ evaluation/; pylint agents/ tools/ orchestration/ api/ evaluation/
    Write-I "Running type checking..."; mypy agents/ tools/ orchestration/ api/ evaluation/
    Write-I "Running tests..."; pytest tests/ -v
    Write-OK "All checks passed"
}
elseif ($Task -eq 'clean') {
    Write-H "Cleaning Cache Files"
    $patterns = @('__pycache__', '*.pyc', '.pytest_cache', '.mypy_cache', '.coverage', 'htmlcov', '*.egg-info', 'dist', 'build')
    foreach ($pattern in $patterns) {
        Get-ChildItem -Path . -Include $pattern -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
    }
    Write-OK "Cache cleaned"
}
elseif ($Task -eq 'run') {
    Write-H "Running Example Workflow"
    python examples/basic_workflow.py
}
elseif ($Task -eq 'run-api') {
    Write-H "Starting FastAPI Server"
    Write-Host "API will be available at: http://localhost:8000" -Fore Green
    Write-Host "API Documentation at: http://localhost:8000/docs" -Fore Green
    Write-Host "Press Ctrl+C to stop the server" -Fore Yellow
    Write-Host ""
    uvicorn examples.fastapi_server:app --reload --host 0.0.0.0 --port 8000
}
else {
    Write-ERR "Unknown task: $Task"
    Write-Host ""
    Write-Host "Available tasks:" -Fore Yellow
    Write-Host "  setup, install, install-dev, test, test-cov, lint, format, type-check, check, clean, run, run-api" -Fore Cyan
    exit 1
}
