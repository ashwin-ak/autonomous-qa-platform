# Quick Start Guide

## 5-Minute Setup

### 1. Install
```bash
# Python 3.11+ required
git clone https://github.com/ashwin-qa/autonomous-qa-platform.git
cd autonomous-qa-platform

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
playwright install
```

### 2. Configure
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key: OPENAI_API_KEY=sk-...
```

### 3. Run (Choose your OS)

**macOS/Linux with Make:**
```bash
make setup      # One-time setup
make run-api    # Start API server
```

**Windows PowerShell:**
```powershell
.\setup-windows.ps1 -Task setup     # One-time setup
.\setup-windows.ps1 -Task run-api   # Start API server
```

**Windows Command Prompt:**
```cmd
setup-windows.bat setup     # One-time setup
setup-windows.bat run-api   # Start API server
```

## OS-Specific Commands

### Available Tasks

| Task | macOS/Linux | Windows PS | Windows CMD |
|------|-----------|-----------|-----------|
| Setup | `make setup` | `.\setup-windows.ps1 -Task setup` | `setup-windows.bat setup` |
| Install | `make install` | `.\setup-windows.ps1 -Task install` | `setup-windows.bat install` |
| Run Example | `make run` | `.\setup-windows.ps1 -Task run` | `setup-windows.bat run` |
| Run API | `make run-api` | `.\setup-windows.ps1 -Task run-api` | `setup-windows.bat run-api` |
| Tests | `make test` | `.\setup-windows.ps1 -Task test` | `setup-windows.bat test` |
| Lint | `make lint` | `.\setup-windows.ps1 -Task lint` | `setup-windows.bat lint` |
| Format | `make format` | `.\setup-windows.ps1 -Task format` | `setup-windows.bat format` |
| Type Check | `make type-check` | `.\setup-windows.ps1 -Task type-check` | `setup-windows.bat type-check` |

## Common Use Cases

### Use Case 1: Generate Tests for a Feature

```python
from orchestration.agent_workflow import AutonomousQAWorkflow

workflow = AutonomousQAWorkflow()

feature = "User authentication with email/password"
result = workflow.run_qa_workflow(feature)

print(f"Test Plan: {result.test_plan}")
print(f"Success: {result.success}")
```

### Use Case 2: Run as Web API

```bash
# Start server
uvicorn examples.fastapi_server:app --port 8000

# In another terminal, test it
curl -X POST http://localhost:8000/api/qa/run \
  -H "Content-Type: application/json" \
  -d '{"feature_description":"Login feature"}'
```

### Use Case 3: Just Generate Test Plan (No Execution)

```python
from agents.test_plan_agent import TestPlanAgent

agent = TestPlanAgent()
test_plan = agent.generate_test_plan("Your feature description here")
print(test_plan)
```

### Use Case 4: CI/CD Integration

```bash
# In your CI/CD pipeline
python examples/basic_workflow.py

# Exit code 0 = all tests passed
# Exit code 1 = tests failed
```

## File Organization

After setup, your project structure looks like:

```
autonomous-qa-platform/
├── .env                              # Your configuration (SECRET - don't commit)
├── agents/                           # Test planning and analysis agents
├── tools/                            # Test runners and log parsers
├── orchestration/                    # Main workflow
├── playwright-tests/tests/generated  # Auto-generated tests
├── logs/                             # Execution logs
└── examples/                         # Usage examples
```

## Next Steps

1. **Read**: [Full Documentation](README.md)
2. **Learn**: [Architecture](docs/architecture.md)
3. **Configure**: [Advanced Settings](docs/configuration.md)
4. **Develop**: [Contributing](CONTRIBUTING.md)
5. **Deploy**: [API Reference](docs/api.md)

## Troubleshooting

### ❌ "OPENAI_API_KEY not found"
```
✓ Solution: Create .env file with OPENAI_API_KEY=sk-...
```

### ❌ "Playwright browsers not found"
```
✓ Solution: Run `playwright install`
```

### ❌ "Module not found: orchestration"
```
✓ Solution: Run from project root directory
✓ Solution: Ensure virtual environment is activated
```

### ❌ "Port 8000 already in use"
```
✓ Solution: Use different port: --port 8001
```

## Development Checklist

- [ ] Python 3.11+ installed
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Playwright installed (`playwright install`)
- [ ] `.env` file created with OpenAI key
- [ ] Example workflow runs successfully

## Useful Commands

```bash
# Run tests
pytest tests/

# Format code
black agents/ tools/ orchestration/

# Check for errors
mypy agents/

# View API documentation
# Open http://localhost:8000/docs

# Generate test plan only
python -c "from agents.test_plan_agent import TestPlanAgent; TestPlanAgent().generate_test_plan('your feature')"
```

## Learning Resources

- **Official Docs**: See `docs/` folder
- **Code Examples**: See `examples/` folder
- **API Docs**: Start server and visit `/docs`
- **Architecture**: Read `docs/architecture.md`

## Support

- 📖 Check [Documentation](README.md)
- 🐛 Report [Issues](https://github.com/ashwin-qa/autonomous-qa-platform/issues)
- 💬 Start [Discussion](https://github.com/ashwin-qa/autonomous-qa-platform/discussions)

## Getting Help

```bash
# Show all available commands
make help

# Install everything with one command
make setup

# Run all checks
make check
```

Happy testing! 🚀