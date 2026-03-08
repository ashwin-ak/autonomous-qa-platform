# Windows Setup Instructions

You received an error message:
```
The term 'make' is not recognized as the name of a cmdlet
```

This is **expected on Windows**. The `make` command is a Unix/Linux tool and is not available by default on Windows.

## ✅ Solution: Use Windows Setup Scripts

I've created two setup scripts for Windows users:

### Option 1: PowerShell (Recommended)

**First time setup:**
```powershell
# Open PowerShell in the project directory
cd c:\Ashwin\AI\code\autonomous-qa-platform

# Run the setup script
.\setup-windows.ps1 -Task setup
```

**Common commands:**
```powershell
.\setup-windows.ps1 -Task run-api      # Start API server
.\setup-windows.ps1 -Task run          # Run example
.\setup-windows.ps1 -Task test         # Run tests
.\setup-windows.ps1 -Task format       # Format code
.\setup-windows.ps1 -Task check        # All quality checks
```

**If you get an execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then run the setup again.

### Option 2: Command Prompt

**First time setup:**
```cmd
cd c:\Ashwin\AI\code\autonomous-qa-platform
setup-windows.bat setup
```

**Common commands:**
```cmd
setup-windows.bat run-api      # Start API server
setup-windows.bat run          # Run example
setup-windows.bat test         # Run tests
setup-windows.bat format       # Format code
setup-windows.bat check        # All quality checks
```

## 📋 What Each Script Does

### setup
- Installs all Python dependencies
- Installs Playwright browsers
- Creates required directories
- Creates .env file from template
- ✅ Recommended for first time!

### install
- Installs core Python dependencies only

### install-dev
- Installs dev dependencies (testing, linting, etc.)

### run-api
- Starts FastAPI server at http://localhost:8000
- Documentation at http://localhost:8000/docs

### run
- Runs the example workflow

### test
- Runs unit tests with pytest

### test-cov
- Tests with coverage report (generates htmlcov/index.html)

### lint
- Checks code style with flake8 and pylint

### format
- Formats code with black and isort

### check
- Runs all quality checks (lint + type + tests)

## 🚀 Quick Start (5 minutes)

### PowerShell users:
```powershell
# 1. Navigate to project
cd autonomous-qa-platform

# 2. Run setup
.\setup-windows.ps1 -Task setup

# 3. Edit .env file with your OpenAI API key
# Open .env in your editor and add: OPENAI_API_KEY=sk-...

# 4. Start API server
.\setup-windows.ps1 -Task run-api

# 5. Open browser
# http://localhost:8000/docs
```

### Command Prompt users:
```cmd
# 1. Navigate to project
cd autonomous-qa-platform

# 2. Run setup
setup-windows.bat setup

# 3. Edit .env file with your OpenAI API key

# 4. Start API server
setup-windows.bat run-api

# 5. Open browser
# http://localhost:8000/docs
```

## 📝 What You Need To Do Now

1. **Choose your script** (PowerShell or Command Prompt)
2. **Run the setup**:
   - PowerShell: `.\setup-windows.ps1 -Task setup`
   - Command Prompt: `setup-windows.bat setup`
3. **Edit .env** file with your OpenAI API key
4. **Start the API**: `.\setup-windows.ps1 -Task run-api`
5. **Visit**: http://localhost:8000/docs

## Advanced: Manual Installation

If you prefer to run commands manually:

```cmd
REM Create virtual environment
python -m venv venv
venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

REM Install Playwright
playwright install

REM Create directories
mkdir logs data\chromadb data\persist playwright-tests\tests\generated

REM Copy environment file
copy .env.example .env

REM Edit .env with your API key
# Open .env in any editor and add your OpenAI API key

REM Run tests
python -m pytest tests/ -v

REM Start API
uvicorn examples.fastapi_server:app --reload --host 0.0.0.0 --port 8000
```

## 🆘 Troubleshooting

### PowerShell: "Cannot be loaded because running scripts is disabled"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then run the script again.

### Error: "python not found"
Make sure Python 3.11+ is installed and in your PATH:
```cmd
python --version
```

Should show Python 3.11 or higher.

### Error: "pip not found"
Use the module directly:
```cmd
python -m pip install -r requirements.txt
```

### Error: "playwright not found after install"
Try installing with dependencies:
```cmd
playwright install --with-deps
```

### API won't start
Make sure port 8000 isn't already in use:
```cmd
# Try a different port
uvicorn examples.fastapi_server:app --port 8001
```

## 📚 More Information

- **Main README**: [README.md](README.md)
- **Windows Guide**: [WINDOWS_SETUP.md](WINDOWS_SETUP.md)
- **Installation Help**: [INSTALL.md](INSTALL.md)
- **Configuration**: [docs/configuration.md](docs/configuration.md)
- **API Docs**: [docs/api.md](docs/api.md)

## 💬 Need Help?

If you encounter issues:
1. Check [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for detailed Windows guide
2. Review [INSTALL.md](INSTALL.md) for troubleshooting
3. Check `.env` file has your OpenAI API key
4. Make sure Python 3.11+ is installed

---

**Remember**: On Windows, use `.\setup-windows.ps1` or `setup-windows.bat` instead of `make` commands.

Happy testing! 🚀