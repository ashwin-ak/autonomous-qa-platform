@echo off
REM Autonomous QA Platform - Windows Setup Script (CMD version)
REM This is an alternative for users who don't use PowerShell
REM Run: setup-windows.bat on command prompt

setlocal enabledelayedexpansion
set TASK=%1
if "%TASK%"=="" set TASK=setup

:setup
if "%TASK%"=="setup" (
    echo.
    echo ========================================
    echo Autonomous QA Platform - Complete Setup
    echo ========================================
    echo.
    
    echo Installing dev dependencies...
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    
    echo.
    echo Installing Playwright browsers...
    playwright install
    
    echo.
    echo Creating directories...
    if not exist logs mkdir logs
    if not exist data\chromadb mkdir data\chromadb
    if not exist data\persist mkdir data\persist
    if not exist playwright-tests\tests\generated mkdir playwright-tests\tests\generated
    
    echo.
    echo Setting up environment...
    if not exist .env (
        copy .env.example .env
        echo.
        echo ✓ Created .env file
        echo.
        echo IMPORTANT: Edit .env and add your OpenAI API key:
        echo   OPENAI_API_KEY=sk-...
    )
    
    echo.
    echo ✓ Setup Complete!
    echo.
    echo Next steps:
    echo 1. Edit .env with your OpenAI API key
    echo 2. Run tests: setup-windows.bat test
    echo 3. Run API: setup-windows.bat run-api
    echo.
    goto :eof
)

if "%TASK%"=="install" (
    echo Installing dependencies...
    pip install -r requirements.txt
    goto :eof
)

if "%TASK%"=="install-dev" (
    echo Installing dev dependencies...
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    goto :eof
)

if "%TASK%"=="test" (
    echo Running tests...
    pytest tests/ -v
    goto :eof
)

if "%TASK%"=="test-cov" (
    echo Running tests with coverage...
    pytest tests/ -v --cov=agents,tools,orchestration --cov-report=html --cov-report=term
    echo.
    echo Coverage report generated in htmlcov/index.html
    goto :eof
)

if "%TASK%"=="lint" (
    echo Running linting...
    flake8 agents/ tools/ orchestration/ api/ evaluation/
    pylint agents/ tools/ orchestration/ api/ evaluation/
    goto :eof
)

if "%TASK%"=="format" (
    echo Formatting code...
    black agents/ tools/ orchestration/ api/ evaluation/ examples/
    isort agents/ tools/ orchestration/ api/ evaluation/ examples/
    echo.
    echo ✓ Code formatted
    goto :eof
)

if "%TASK%"=="type-check" (
    echo Running type checking...
    mypy agents/ tools/ orchestration/ api/ evaluation/
    goto :eof
)

if "%TASK%"=="check" (
    echo Running all checks...
    flake8 agents/ tools/ orchestration/ api/ evaluation/
    pylint agents/ tools/ orchestration/ api/ evaluation/
    mypy agents/ tools/ orchestration/ api/ evaluation/
    pytest tests/ -v
    echo.
    echo ✓ All checks passed
    goto :eof
)

if "%TASK%"=="clean" (
    echo Cleaning cache files...
    for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
    for /r . %%f in (*.pyc) do @if exist "%%f" del /q "%%f"
    if exist .pytest_cache rd /s /q .pytest_cache
    if exist .mypy_cache rd /s /q .mypy_cache
    if exist htmlcov rd /s /q htmlcov
    echo.
    echo ✓ Cache cleaned
    goto :eof
)

if "%TASK%"=="run" (
    echo Running example workflow...
    python examples/basic_workflow.py
    goto :eof
)

if "%TASK%"=="run-api" (
    echo.
    echo ========================================
    echo Starting FastAPI Server
    echo ========================================
    echo.
    echo API available at: http://localhost:8000
    echo Docs available at: http://localhost:8000/docs
    echo.
    echo Press Ctrl+C to stop
    echo.
    uvicorn examples.fastapi_server:app --reload --host 0.0.0.0 --port 8000
    goto :eof
)

echo Unknown task: %TASK%
echo.
echo Available tasks:
echo   setup       - Complete setup (default)
echo   install     - Install dependencies
echo   install-dev - Install dev dependencies
echo   test        - Run tests
echo   test-cov    - Tests with coverage
echo   lint        - Linting checks
echo   format      - Code formatting
echo   type-check  - Type checking
echo   check       - All quality checks
echo   clean       - Clean cache files
echo   run         - Run example
echo   run-api     - Start API server
