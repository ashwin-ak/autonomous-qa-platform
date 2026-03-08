# Development Guide

**Author:** Ashwin Kulkarni  
**License:** MIT

## Setting Up Development Environment

### Prerequisites
- Python 3.11+
- Git
- Node.js 18+ (for Playwright)
- Virtual environment tool (venv, conda, etc.)

### Initial Setup

```bash
# Clone the repository
git clone <repo-url>
cd autonomous-qa-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies (with dev extras)
pip install -r requirements/requirements.txt
pip install -r requirements/requirements-dev.txt

# Install Playwright browsers
playwright install

# Set up pre-commit hooks (optional)
pip install pre-commit
pre-commit install

# Configure environment
cp .env.example .env
# Edit .env with your development settings
```

## Project Structure Explanation

```
autonomous-qa-platform/
├── agents/                          # LLM agents
│   ├── test_plan_agent.py          # Test plan generation
│   ├── test_generation_agent.py    # Test code generation
│   └── rca_agent.py                # Root cause analysis
├── tools/                           # Utilities
│   ├── playwright_runner.py        # Test execution
│   └── log_parser.py               # Log extraction
├── orchestration/                   # Workflow
│   └── agent_workflow.py           # Main orchestrator
├── api/                             # API package
│   └── __init__.py
├── rag/                             # Vector DB
│   ├── embeddings.py               # Embedding generation
│   └── vector_store.py             # Vector DB operations
├── prompts/                         # LLM prompts
│   ├── test_plan_prompt.txt
│   └── rca_prompt.txt
├── evaluation/                      # Metrics
│   └── agent_metrics.py            # Performance metrics
├── playwright-tests/                # Test files
│   └── tests/
│       └── generated/               # Auto-generated tests
├── config/                          # Configuration
│   └── config.yaml                 # Default config
├── examples/                        # Usage examples
│   ├── basic_workflow.py
│   └── fastapi_server.py
├── tests/                           # Unit tests
│   ├── test_agents.py
│   ├── test_tools.py
│   └── test_workflow.py
├── docs/                            # Documentation
│   ├── architecture.md
│   ├── configuration.md
│   ├── api.md
│   └── development.md
├── requirements/                    # Dependencies
│   ├── requirements.txt
│   └── requirements-dev.txt
```

## Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/add-new-agent
```

### 2. Make Changes
- Follow PEP 8 style guide
- Add type hints
- Write docstrings
- Add unit tests

### 3. Test Your Changes
```bash
# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=. tests/

# Type checking
mypy agents/ tools/ orchestration/

# Linting
pylint agents/ tools/ orchestration/

# Code formatting
black agents/ tools/ orchestration/
```

### 4. Commit and Push
```bash
git add .
git commit -m "feat: add new agent for API testing"
git push origin feature/add-new-agent
```

### 5. Create Pull Request
- Describe changes clearly
- Reference related issues
- Ensure CI passes
- Request review from maintainers

## Code Style Guidelines

### Python Style
- Follow PEP 8
- Use type hints for all functions
- Max line length: 100 characters
- Use f-strings for formatting

```python
def generate_test_plan(
    self, 
    feature_description: str,
    max_tests: int = 10
) -> Dict[str, List[str]]:
    """
    Generate a test plan from feature description.
    
    Args:
        feature_description: Description of the feature to test
        max_tests: Maximum number of tests to generate
        
    Returns:
        Dictionary with test categories and scenarios
        
    Raises:
        ValueError: If feature_description is empty
    """
    if not feature_description:
        raise ValueError("Feature description cannot be empty")
    
    # Implementation
    return {}
```

### Docstring Format
Use Google-style docstrings:

```python
def method_name(param1: str, param2: int) -> bool:
    """Brief description of the method.
    
    Longer description if needed. Can span multiple
    lines with more details about behavior.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When validation fails
        TimeoutError: When operation times out
    """
```

### Type Hints
Always use type hints:

```python
from typing import Dict, List, Optional, Tuple

def process_logs(
    stdout: str,
    stderr: str,
    max_lines: Optional[int] = None
) -> Tuple[List[str], List[str]]:
    """Process logs and return errors and traces."""
    pass
```

## Adding New Agents

### Step 1: Create Agent File
Create `agents/custom_agent.py`:

```python
import os
import logging
from typing import Dict, Any
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

logger = logging.getLogger(__name__)

class CustomOutput(BaseModel):
    result: str = Field(description="The result")
    confidence: float = Field(description="Confidence score")

class CustomAgent:
    def __init__(
        self,
        model_name: str = "gpt-4o",
        temperature: float = 0.1,
        max_retries: int = 3
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.max_retries = max_retries
        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.parser = JsonOutputParser(pydantic_object=CustomOutput)
        self.prompt = PromptTemplate(
            template="Your prompt here: {input}",
            input_variables=["input"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )
        self.chain = self.prompt | self.llm | self.parser

    def process(self, input_data: str) -> Dict[str, Any]:
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Processing, attempt {attempt + 1}")
                result = self.chain.invoke({"input": input_data})
                return result
            except Exception as e:
                logger.error(f"Error on attempt {attempt + 1}: {e}")
                if attempt == self.max_retries - 1:
                    raise e
        return {}
```

### Step 2: Integrate into Workflow

Update `orchestration/agent_workflow.py`:

```python
from agents.custom_agent import CustomAgent

class AutonomousQAWorkflow:
    def __init__(self):
        # ... existing agents ...
        self.custom_agent = CustomAgent()
    
    def run_qa_workflow(self, feature_description: str) -> QAResult:
        # ... existing steps ...
        
        # Add new step
        custom_result = self.custom_agent.process(feature_description)
        # ... rest of workflow ...
```

### Step 3: Write Tests

Create `tests/test_custom_agent.py`:

```python
import pytest
from agents.custom_agent import CustomAgent

@pytest.fixture
def agent():
    return CustomAgent()

def test_custom_agent_initialization(agent):
    assert agent.model_name == "gpt-4o"
    assert agent.temperature == 0.1

def test_custom_agent_process(agent):
    result = agent.process("test input")
    assert "result" in result
    assert "confidence" in result
```

## Useful Commands

### Linux/macOS (with Make)
```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_agents.py::test_test_plan_agent

# Run with verbose output
pytest -v tests/

# Run with coverage
pytest --cov=agents --cov=tools tests/
```

### Windows (PowerShell)
```powershell
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_agents.py::test_test_plan_agent

# Run with verbose output
python -m pytest -v tests/

# Run with coverage
python -m pytest --cov=agents --cov=tools tests/
```

### Windows (Command Prompt)
```cmd
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_agents.py::test_test_plan_agent

# Run with verbose output
python -m pytest -v tests/

# Run with coverage
python -m pytest --cov=agents --cov=tools tests/
```

### Integration Tests
```bash
# Run integration tests
pytest tests/integration/

# Run workflow end-to-end
python examples/basic_workflow.py
```

### Test Coverage Goals
- Agents: 85%+ coverage
- Tools: 80%+ coverage
- Orchestration: 90%+ coverage

## Debugging

### Enable Debug Logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

### Use Python Debugger
```python
import pdb; pdb.set_trace()  # Older Python
# Or in Python 3.7+
breakpoint()
```

### Check Agent Outputs
```python
from orchestration.agent_workflow import AutonomousQAWorkflow

workflow = AutonomousQAWorkflow()
result = workflow.run_qa_workflow("test feature")

# Inspect outputs
print(f"Test Plan: {result.test_plan}")
print(f"Test Results: {result.test_results}")
if result.rca_results:
    print(f"RCA: {result.rca_results}")
```

## Performance Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 functions
```

## Common Issues

### Issue: ModuleNotFoundError
```
Error: No module named 'agents'
→ Solution: Run from project root directory
→ Solution: Add project to PYTHONPATH
```

### Issue: OpenAI API Errors
```
Error: Invalid API Key
→ Solution: Check OPENAI_API_KEY in .env
→ Solution: Ensure key is active on OpenAI dashboard

Error: Rate Limit Exceeded
→ Solution: Increase delay between requests
→ Solution: Use exponential backoff (already implemented)
```

### Issue: Playwright Timeouts
```
Error: Timeout waiting for element
→ Solution: Increase PLAYWRIGHT_TIMEOUT
→ Solution: Check selector validity
→ Solution: Add explicit waits
```

## Contributing

### Before Submitting PR
- [ ] Code follows PEP 8
- [ ] Type hints added
- [ ] Docstrings updated
- [ ] Unit tests added
- [ ] Tests passing (pytest)
- [ ] No linting errors (pylint, flake8)
- [ ] Code formatted (black)
- [ ] Coverage maintained (85%+)

### Commit Message Format
```
type(scope): subject

body

footer
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`

Examples:
```
feat(agents): add custom agent support
fix(tools): fix log parser regex pattern
docs(readme): update installation steps
test(workflow): add integration tests
```

## Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Playwright Documentation](https://playwright.dev/python/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)