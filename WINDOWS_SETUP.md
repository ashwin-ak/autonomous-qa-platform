# Windows Setup Guide

If you're on Windows, you cannot use the `make` command (which is designed for Unix/Linux). Instead, use one of the provided setup scripts.

## Option 1: PowerShell (Recommended)

PowerShell is built into Windows and provides the most features.

### Running Setup
```powershell
# Navigate to project directory
cd autonomous-qa-platform

# First time full setup
.\setup-windows.ps1 -Task setup

# Or run tasks individually
.\setup-windows.ps1 -Task install
.\setup-windows.ps1 -Task run-api
```

### Available Tasks
```
setup       - Complete setup with all dependencies
install     - Install core dependencies
install-dev - Install development dependencies
test        - Run tests
test-cov    - Run tests with coverage report
lint        - Run linting checks
format      - Format code with black and isort
type-check  - Run mypy type checking
check       - Run all quality checks
clean       - Clean cache and build files
run         - Run example workflow
run-api     - Start FastAPI server
```

### Example Commands
```powershell
# First time setup
.\setup-windows.ps1 -Task setup

# Start API server
.\setup-windows.ps1 -Task run-api

# Run tests
.\setup-windows.ps1 -Task test

# Format code
.\setup-windows.ps1 -Task format

# Run all quality checks
.\setup-windows.ps1 -Task check
```

### Troubleshooting PowerShell

**Issue: "script not digitally signed"**
```powershell
# Run this once to allow scripts:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then run the setup script again
.\setup-windows.ps1 -Task setup
```

**Issue: ".ps1 cannot be loaded"**
```powershell
# Make sure you're in the correct directory
cd autonomous-qa-platform

# Then run with full path
.\setup-windows.ps1 -Task setup
```

## Option 2: Command Prompt

Command Prompt is available on all Windows systems with no extra configuration needed.

### Running Setup
```cmd
# Navigate to project directory
cd autonomous-qa-platform

# First time full setup
setup-windows.bat setup

# Or run tasks individually
setup-windows.bat install
setup-windows.bat run-api
```

### Available Tasks
Same as PowerShell:
```
setup, install, install-dev, test, test-cov, lint, format, type-check, check, clean, run, run-api
```

### Example Commands
```cmd
# First time setup
setup-windows.bat setup

# Start API server
setup-windows.bat run-api

# Run tests
setup-windows.bat test

# Format code
setup-windows.bat format

# Run all quality checks
setup-windows.bat check
```

## Option 3: Manual Commands

If you prefer complete control, run commands manually:

```cmd
REM Install dependencies
pip install -r requirements.txt

REM Install dev dependencies
pip install -r requirements-dev.txt

REM Install Playwright browsers
playwright install

REM Create directories
mkdir logs data\chromadb data\persist playwright-tests\tests\generated

REM Copy environment file
copy .env.example .env

REM Run tests
python -m pytest tests/ -v

REM Start API server
uvicorn examples.fastapi_server:app --reload --host 0.0.0.0 --port 8000

REM Run example
python examples/basic_workflow.py
```

## Recommended Workflow

1. **Initial Setup**
   ```powershell
   .\setup-windows.ps1 -Task setup
   ```

2. **Edit Configuration**
   - Open `.env` in your editor
   - Add your OpenAI API key
   - Save the file

3. **Verify Installation**
   ```powershell
   python -c "from orchestration.agent_workflow import AutonomousQAWorkflow; print('✓ OK')"
   ```

4. **Run Example**
   ```powershell
   .\setup-windows.ps1 -Task run
   ```

5. **Start Development**
   ```powershell
   .\setup-windows.ps1 -Task run-api
   
   # In another terminal:
   .\setup-windows.ps1 -Task test
   ```

## Environment Variables

The `.env.example` file contains all configuration options. After setup, edit `.env`:

```env
# Required
OPENAI_API_KEY=sk-your-api-key-here

# Optional
OPENAI_MODEL=gpt-4o
PLAYWRIGHT_TIMEOUT=30000
LOG_LEVEL=INFO
```

## Python Version Check

Make sure you have Python 3.11 or newer:

```cmd
python --version
```

Should output something like: `Python 3.11.0` or higher

## Virtual Environment

The setup scripts automatically work within your virtual environment. Make sure it's activated:

```cmd
REM Activate virtual environment
venv\Scripts\activate

REM You should see (venv) at the start of your prompt
```

## Installation Issues

### Issue: pip command not found
```cmd
python -m pip install -r requirements.txt
```

### Issue: playwright install fails
```cmd
REM Try with administrator privileges
REM Or install browsers individually
playwright install chromium
playwright install firefox
playwright install webkit
```

### Issue: OpenAI API key not recognized
```cmd
REM Make sure .env file is in the correct location
REM Make sure OPENAI_API_KEY=sk-... is set correctly in .env
REM No spaces around the = sign

REM Test if Python can read it:
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY')[:10])"
```

## API Server

Once running, access:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing

Run tests with coverage:
```powershell
.\setup-windows.ps1 -Task test-cov

# Open the coverage report
.\htmlcov\index.html
```

## Development Tools

The script automatically installs tools for:
- Code formatting (`black`, `isort`)
- Linting (`flake8`, `pylint`)
- Type checking (`mypy`)
- Testing (`pytest`, `pytest-cov`)

Use them via the setup script or directly:

```cmd
REM Format code
black agents/ tools/ orchestration/

REM Check types
mypy agents/

REM Lint
flake8 agents/

REM Run tests
pytest tests/ -v
```

## Need Help?

1. Check [README.md](../README.md) for overview
2. Read [INSTALL.md](../INSTALL.md) for installation details
3. See [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines
4. Review [docs/configuration.md](configuration.md) for all settings

## Next Steps

- [ ] Run `.\setup-windows.ps1 -Task setup`
- [ ] Edit `.env` with your OpenAI API key
- [ ] Run `python examples/basic_workflow.py`
- [ ] Start `.\setup-windows.ps1 -Task run-api`
- [ ] Visit http://localhost:8000/docs

Enjoy using Autonomous QA Platform! 🚀