# Contributing to Autonomous QA Platform

**Author:** Ashwin Kulkarni  
**License:** MIT

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Avoid offensive or discriminatory language
- Focus on constructive feedback

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/autonomous-qa-platform.git
   cd autonomous-qa-platform
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements/requirements-dev.txt
   ```
5. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

## Making Changes

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/new-agent` - New features
- `fix/bug-description` - Bug fixes
- `docs/update-readme` - Documentation updates
- `refactor/module-name` - Code refactoring

### 2. Code Style

Follow PEP 8 and these guidelines:

**Type Hints** (Required)
```python
def process(self, data: str, timeout: int = 30) -> Dict[str, Any]:
    """Process data with optional timeout."""
    pass
```

**Docstrings** (Required)
```python
def method(param1: str) -> bool:
    """Brief description here.
    
    Longer description explaining the method's behavior
    and any important details.
    
    Args:
        param1: Description of param1
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When X happens
    """
```

**Max Line Length**: 100 characters

**Naming**:
- Classes: `PascalCase` (e.g., `TestPlanAgent`)
- Functions/Methods: `snake_case` (e.g., `generate_test_plan`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`)
- Private: Prefix with `_` (e.g., `_internal_method`)

### 3. Run Quality Checks

Before committing, run these checks:

```bash
# Format code
black agents/ tools/ orchestration/ api/ evaluation/

# Lint
flake8 agents/ tools/ orchestration/ api/ evaluation/
pylint agents/ tools/ orchestration/ api/ evaluation/

# Type checking
mypy agents/ tools/ orchestration/ api/ evaluation/

# Run tests
pytest tests/ --cov=agents,tools,orchestration

# Sort imports
isort agents/ tools/ orchestration/ api/ evaluation/
```

### 4. Write Tests

For every feature, add tests in `tests/`:

```python
# tests/test_my_feature.py
import pytest
from agents.my_agent import MyAgent

@pytest.fixture
def agent():
    return MyAgent()

def test_basic_functionality(agent):
    """Test basic functionality."""
    result = agent.process("test")
    assert result is not None

def test_error_handling(agent):
    """Test error handling."""
    with pytest.raises(ValueError):
        agent.process("")
```

**Coverage Goals**:
- Agents: 85%+
- Tools: 80%+
- Orchestration: 90%+

### 5. Commit Your Changes

Use meaningful commit messages:

```
feat(agents): add custom agent support

- Implement CustomAgent class
- Add retry logic with exponential backoff
- Add comprehensive docstrings
- Add unit tests for new agent
```

Format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting, missing semicolons)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Build/deployment changes

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a PR on GitHub with:
- Clear description of changes
- Reference any related issues (#123)
- Screenshots for UI changes
- Checklist of tests run

## Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code follows PEP 8 style guide
- [ ] Type hints added to all functions
- [ ] Docstrings added/updated
- [ ] Unit tests added/updated
- [ ] Tests passing: `pytest tests/`
- [ ] No linting errors: `flake8`, `pylint`
- [ ] Code formatted: `black`
- [ ] Imports sorted: `isort`
- [ ] Type checking passes: `mypy`
- [ ] Coverage maintained (85%+)
- [ ] No breaking changes to public API
- [ ] Documentation updated
- [ ] Commits have meaningful messages

## Review Process

1. **Automated Checks**: CI/CD pipeline runs automatically
2. **Code Review**: Maintainers review your PR
3. **Requested Changes**: Address feedback
4. **Approval**: PR approved by maintainers
5. **Merge**: Maintainer merges to main

## Development Workflow Example

```bash
# Create feature branch
git checkout -b feature/add-webhook-support

# Make changes to files

# Run quality checks
black agents/ tools/ orchestration/
pytest tests/
mypy agents/

# Commit changes
git add .
git commit -m "feat(api): add webhook support for job completion"

# Push to GitHub
git push origin feature/add-webhook-support

# Create PR on GitHub (via web interface)
```

## Common Issues

### Issue: Tests failing locally but passing in CI
```
→ Solution: Ensure same Python version (3.11)
→ Solution: Clear .pytest_cache and __pycache__
→ Solution: Reinstall dependencies
```

### Issue: Linting errors
```
→ Solution: Run `black` and `isort` to auto-format
→ Solution: Use VSCode with Pylance extension
```

### Issue: Type checking errors
```
→ Solution: Add type hints to function signatures
→ Solution: Use `Optional[T]` for nullable values
→ Solution: Run `mypy --install-types`
```

## Documentation

For significant changes, update documentation:
- `README.md` - User-facing overview
- `docs/architecture.md` - System design changes
- `docs/api.md` - API endpoint changes
- Code docstrings - For functions and classes

## Questions?

- Open a GitHub discussion
- Check existing issues
- Review documentation in `docs/`
- Look at examples in `examples/`

## License

By contributing, you agree that your contributions will be licensed under the MIT License.