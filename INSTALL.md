# Installation Guide

## System Requirements

- **Python**: 3.11 or higher
- **Node.js**: 18+ (for Playwright)
- **RAM**: 4GB minimum
- **Storage**: 2GB for dependencies and test files

## Quick Start (5 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/ashwin-qa/autonomous-qa-platform.git
cd autonomous-qa-platform
```

### 2. Create Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install Playwright Browsers
```bash
playwright install
```

### 5. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 6. Run Setup Script

**macOS/Linux with Make:**
```bash
make setup
```

**Windows PowerShell:**
```powershell
.\setup-windows.ps1 -Task setup
```

**Windows Command Prompt:**
```cmd
setup-windows.bat setup
```

### 7. Verify Installation
```bash
python -c "from orchestration.agent_workflow import AutonomousQAWorkflow; print('✓ Installation successful!')"
```

## Detailed Installation

### Step 1: Prerequisites

**macOS/Linux**:
```bash
# Check Python version
python3 --version  # Should be 3.11+

# Install Node.js (if not already installed)
brew install node  # macOS
# Or visit https://nodejs.org/

# Install Git (if not already installed)
brew install git  # macOS
```

**Windows**:
```bash
# Download Python 3.11+ from https://python.org
# Download Node.js from https://nodejs.org/
# Download Git from https://git-scm.com/

# Verify installations
python --version
node --version
git --version
```

### Step 2: Clone Repository

```bash
git clone https://github.com/ashwin-qa/autonomous-qa-platform.git
cd autonomous-qa-platform
```

Or using SSH:
```bash
git clone git@github.com:ashwin-qa/autonomous-qa-platform.git
cd autonomous-qa-platform
```

### Step 3: Create Virtual Environment

**Option A: venv (Built-in)**
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**Option B: conda**
```bash
conda create -n qa-platform python=3.11
conda activate qa-platform
```

**Option C: pipenv**
```bash
pipenv install --python 3.11
pipenv shell
```

### Step 4: Install Python Dependencies

```bash
# Upgrade pip, setuptools, wheel
pip install --upgrade pip setuptools wheel

# Install project dependencies
pip install -r requirements.txt

# Optional: Install development dependencies
pip install -r requirements-dev.txt
```

### Step 5: Install Playwright Browsers

```bash
playwright install
# This downloads Chromium, Firefox, and WebKit browsers
```

Or specific browsers:
```bash
playwright install chromium        # Chromium only
playwright install firefox         # Firefox only
playwright install webkit          # WebKit only
```

### Step 6: Create Environment File

```bash
# Copy example file
cp .env.example .env

# Edit with your settings
# On macOS/Linux:
nano .env

# On Windows:
notepad .env
```

**Required Variables**:
```env
OPENAI_API_KEY=sk-...              # Your OpenAI API key (required)
```

**Optional Variables**:
```env
OPENAI_MODEL=gpt-4o
PLAYWRIGHT_TIMEOUT=30000
LOG_LEVEL=INFO
```

### Step 7: Create Required Directories

```bash
mkdir -p logs
mkdir -p data/chromadb
mkdir -p data/persist
mkdir -p playwright-tests/tests/generated
```

### Step 8: Verify Installation

```bash
# Test imports
python -c "from orchestration.agent_workflow import AutonomousQAWorkflow; print('✓ Installation successful')"

# Run basic workflow
python examples/basic_workflow.py

# Or start API server
uvicorn examples.fastapi_server:app --reload
```

## Installing with Docker

### Using Docker

```bash
# Build image
docker build -t autonomous-qa:latest .

# Run container
docker run -it \
  -e OPENAI_API_KEY=sk-... \
  -v $(pwd)/playwright-tests:/app/playwright-tests \
  -v $(pwd)/logs:/app/logs \
  autonomous-qa:latest

# Run with API server
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=sk-... \
  autonomous-qa:latest \
  uvicorn examples.fastapi_server:app --host 0.0.0.0
```

### Using Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  qa-platform:
    build: .
    environment:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    ports:
      - "8000:8000"
    volumes:
      - ./playwright-tests:/app/playwright-tests
      - ./logs:/app/logs
```

```bash
docker-compose up
```

## Troubleshooting Installation

### Issue: Python version too old
```
Error: Python 3.11+ required
→ Solution: Install Python 3.11 from python.org
→ Solution: Use pyenv for version management
```

### Issue: pip command not found
```
Error: command not found: pip
→ Solution: Use `python -m pip` instead
→ Solution: Check Python installation path
```

### Issue: Virtual environment not activating
```
Error: source: command not found (Windows)
→ Solution: Use `venv\Scripts\activate`
→ Solution: Use PowerShell if using cmd.exe
```

### Issue: Missing API key
```
Error: OPENAI_API_KEY not found
→ Solution: Create .env file with API key
→ Solution: Run `cp .env.example .env`
→ Solution: Add key to system environment variables
```

### Issue: Playwright browsers not installing
```
Error: Playwright browsers not found
→ Solution: Run `playwright install`
→ Solution: Check disk space (browsers need ~800MB)
→ Solution: Try `playwright install --with-deps`
```

### Issue: Port 8000 already in use
```
Error: Address already in use
→ Solution: Use different port: `uvicorn examples.fastapi_server:app --port 8001`
→ Solution: Kill process using port: `lsof -ti:8000 | xargs kill -9`
```

## Updating Installation

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update Playwright browsers
playwright install --with-deps

# Check for updates
pip list --outdated
```

## Uninstalling

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# Or if using conda
conda deactivate
conda remove --name qa-platform --all
```

## Next Steps

After installation, try:

1. **Run basic workflow**: `python examples/basic_workflow.py`
2. **Start API server**: `uvicorn examples.fastapi_server:app --reload`
3. **Read documentation**: Check `docs/` folder
4. **Run tests**: `pytest tests/`
5. **View API docs**: Open http://localhost:8000/api/docs

## Support

If you encounter issues:

1. Check [Troubleshooting](#troubleshooting-installation) section above
2. Review [Configuration Guide](docs/configuration.md)
3. Check existing [GitHub Issues](https://github.com/ashwin-qa/autonomous-qa-platform/issues)
4. Read [Development Guide](docs/development.md)
5. Open a new GitHub issue with details