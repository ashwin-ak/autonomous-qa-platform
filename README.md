# Autonomous QA Platform

An enterprise-grade, AI-driven Autonomous QA platform that automatically generates, executes, and analyzes test cases using LLM agents. Built with LangChain, OpenAI, and Playwright.

## Overview

The Autonomous QA Platform automates the entire QA process:

1. **Test Planning**: Parse feature descriptions and generate structured test plans
2. **Test Generation**: Convert test plans into executable Playwright tests  
3. **Test Execution**: Run tests and capture detailed results
4. **Root Cause Analysis**: Analyze failures and provide actionable insights

## Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key
- Node.js 18+ (for Playwright)

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd autonomous-qa-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Setup (choose based on your OS)

# macOS/Linux:
make setup

# Windows PowerShell:
.\setup-windows.ps1 -Task setup

# Windows Command Prompt:
setup-windows.bat setup
```

Or install manually:
```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Configure environment
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

### Basic Workflow

```python
from orchestration.agent_workflow import AutonomousQAWorkflow

# Initialize workflow
workflow = AutonomousQAWorkflow()

# Run QA on a feature
feature_description = """
Implement a user login feature with:
- Email/password authentication
- Remember me functionality
- Password reset via email
- Account lockout after 5 failed attempts
"""

result = workflow.run_qa_workflow(feature_description)

# Access results
print(f"Test Plan: {result.test_plan}")
print(f"Success: {result.success}")
if result.rca_results:
    print(f"RCA: {result.rca_results}")
```

### With FastAPI

See [examples/fastapi_server.py](examples/fastapi_server.py) for running as a web service.

## Architecture

The platform consists of four main components:

### 1. Agents (`agents/`)
- **TestPlanAgent**: Generates structured test plans from feature descriptions
- **TestGenerationAgent**: Creates Playwright test code from test plans
- **RCAAgent**: Performs root cause analysis on test failures

### 2. Tools (`tools/`)
- **PlaywrightRunner**: Executes Playwright tests and captures results
- **LogParser**: Extracts and structures error information from test logs

### 3. Orchestration (`orchestration/`)
- **AutonomousQAWorkflow**: Main workflow orchestrator
- **QAResult**: Structured output containing test plan, results, and RCA

### 4. Infrastructure
- **RAG** (`rag/`): Vector database and embeddings for context retrieval
- **Prompts** (`prompts/`): LLM prompt templates
- **Evaluation** (`evaluation/`): Performance metrics and evaluation tools
- **API** (`api/`): FastAPI server for HTTP endpoints

See [docs/architecture.md](docs/architecture.md) for detailed architecture.

## Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
OPENAI_API_KEY=sk-...
PLAYWRIGHT_TIMEOUT=30000
LOG_LEVEL=INFO
```

See [docs/configuration.md](docs/configuration.md) for all options.

## Project Structure

```
autonomous-qa-platform/
├── agents/                          # LLM agents
│   ├── test_plan_agent.py
│   ├── test_generation_agent.py
│   └── rca_agent.py
├── tools/                           # Utilities and runners
│   ├── playwright_runner.py
│   └── log_parser.py
├── orchestration/                   # Workflow orchestration
│   └── agent_workflow.py
├── api/                             # API package
│   └── __init__.py
├── rag/                             # Vector DB and embeddings
│   ├── embeddings.py
│   └── vector_store.py
├── prompts/                         # LLM prompt templates
│   ├── test_plan_prompt.txt
│   └── rca_prompt.txt
├── evaluation/                      # Evaluation metrics
│   └── agent_metrics.py
├── playwright-tests/                # Test files
│   └── tests/
│       └── generated/               # Auto-generated tests
├── config/                          # Configuration templates
│   └── config.yaml
├── examples/                        # Usage examples
│   ├── basic_workflow.py
│   └── fastapi_server.py
├── tests/                           # Unit tests
├── docs/                            # Documentation
│   ├── architecture.md
│   ├── configuration.md
│   ├── api.md
│   └── development.md
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
├── README.md                        # This file
└── LICENSE
```

## Documentation

- [Architecture](docs/architecture.md) - System design and data flow
- [Configuration](docs/configuration.md) - Environment and settings
- [API Reference](docs/api.md) - HTTP API documentation
- [Development Guide](docs/development.md) - Contributing guidelines
- [Examples](examples/) - Code samples and usage patterns

## Features

- ✅ **AI-Powered Test Planning**: Intelligent test scenario generation
- ✅ **Automatic Test Generation**: TypeScript/JavaScript Playwright tests
- ✅ **Test Execution**: Concurrent test runs with detailed reporting
- ✅ **Failure Analysis**: Root cause analysis powered by LLMs
- ✅ **JSON Structured Output**: Machine-readable results
- ✅ **Retry Logic**: Automatic retries with exponential backoff
- ✅ **Error Handling**: Comprehensive error handling and logging
- ✅ **Extensible Architecture**: Easy to add custom agents and tools

## Tech Stack

- **Python 3.11**: Backend language
- **LangChain**: LLM framework and orchestration
- **OpenAI GPT-4**: Intelligence engine
- **Playwright**: Browser automation
- **FastAPI**: REST API framework
- **ChromaDB**: Vector database for RAG
- **Pydantic**: Data validation

## Performance

- Average test plan generation: < 10 seconds
- Average test generation: < 30 seconds
- Parallel test execution: Depends on test count and complexity
- RCA analysis: < 5 seconds per failure

## Contributing

See [docs/development.md](docs/development.md) for setup and contribution guidelines.

## License

MIT License - see [LICENSE](LICENSE) file

## Support

For issues, questions, or contributions, please open a GitHub issue.
