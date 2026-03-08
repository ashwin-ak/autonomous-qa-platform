# Architecture

## System Overview

The Autonomous QA Platform follows a multi-agent orchestration pattern with clear separation of concerns.

```
┌─────────────────────────────────────────────────────────────┐
│                      User Application                        │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│          AutonomousQAWorkflow (Orchestrator)                 │
└──────────────┬──────────────┬──────────────┬────────────────┘
               │              │              │
       ┌───────▼────┐  ┌──────▼──────┐  ┌───▼─────────┐
       │ TestPlan   │  │    Test     │  │ Playwright  │
       │   Agent    │  │ Generation  │  │   Runner    │
       │            │  │   Agent     │  │             │
       └────────────┘  └─────────────┘  └─────────────┘
            ▲                │                │
            │                ▼                ▼
    ┌───────┴──────┐  ┌──────────────┐  ┌──────────────┐
    │   OpenAI     │  │  OpenAI      │  │   Test       │
    │   GPT-4      │  │  GPT-4       │  │   Results    │
    └──────────────┘  └──────────────┘  └─────┬────────┘
                                              │
                                        ┌─────▼─────────┐
                                        │   Log Parser  │
                                        └────────┬──────┘
                                                 │
                                        ┌────────▼──────┐
                                        │   RCA Agent   │
                                        │   (OpenAI)    │
                                        └───────────────┘
```

## Core Components

### 1. Agents

#### TestPlanAgent
- **Purpose**: Generate comprehensive test plans from feature descriptions
- **Input**: Feature description (string)
- **Output**: Structured test plan (JSON)
  ```json
  {
    "functional_tests": ["Test scenario 1", "Test scenario 2"],
    "edge_cases": ["Edge case 1", "Edge case 2"],
    "api_tests": ["API test 1", "API test 2"],
    "ui_tests": ["UI test 1", "UI test 2"]
  }
  ```
- **LLM**: OpenAI GPT-4
- **Retry Logic**: 3 attempts with exponential backoff
- **Schema Validation**: Pydantic `TestPlan` model

#### TestGenerationAgent
- **Purpose**: Convert test plans into executable Playwright tests
- **Input**: Test plan (JSON)
- **Output**: Playwright TypeScript test files (Dict[filename -> content])
- **Features**:
  - Page Object Model pattern
  - Proper error handling
  - Assertions and validations
  - Supports UI and API tests
- **Retry Logic**: 3 attempts
- **Output Format**: JSON with test files as values

#### RCAAgent
- **Purpose**: Analyze test failures and provide root cause analysis
- **Input**:
  - Test failures (list of strings)
  - Full logs (string)
  - Stack traces (string)
- **Output**: RCA result
  ```json
  {
    "root_cause": "Element not found in DOM",
    "suspected_module": "LoginForm component",
    "suggested_fix": "Wait for element with explicit wait",
    "confidence_score": 0.95
  }
  ```
- **Retry Logic**: 3 attempts
- **Schema Validation**: Pydantic `RCAResult` model

### 2. Tools

#### PlaywrightRunner
- **Purpose**: Execute Playwright tests in subprocess
- **Features**:
  - Timeout handling (default: 5 minutes)
  - Captures stdout and stderr
  - Returns exit code
- **Configuration**:
  - Test directory: `playwright-tests/`
  - timeout: 300000ms
- **Output**: (stdout, stderr, return_code)

#### LogParser
- **Purpose**: Extract and structure error information from logs
- **Methods**:
  - `extract_errors()`: Find error messages using regex
  - `extract_stack_traces()`: Parse stack traces
  - `extract_exceptions()`: Extract exception details
  - `format_logs_for_ai()`: Prepare logs for LLM analysis
- **Regex Patterns**:
  - Error pattern: `/ERROR|Error|error|FAIL|fail/i`
  - Stack trace pattern: `/at\s+.*?\(.*?\)/m`
  - Exception pattern: `/(Exception|Error):\s*(.*?)(?:\n|$)/i`

### 3. Orchestrator

#### AutonomousQAWorkflow
- **Workflow Steps**:
  1. Generate test plan (`test_plan_agent.generate_test_plan()`)
  2. Generate tests (`test_generation_agent.generate_tests()`)
  3. Write test files (`_write_test_files()`)
  4. Execute tests (`playwright_runner.run_tests()`)
  5. Parse results (`log_parser.format_logs_for_ai()`)
  6. If failures → Run RCA (`rca_agent.analyze_failures()`)

- **Error Handling**: Try-catch at workflow level with logging
- **Output**: `QAResult` object containing test plan, results, and RCA

## Data Flow

```
Feature Description
       │
       ▼
Test Plan Agent ──────────► Test Plan (JSON)
       │                         │
       │                         ▼
       │                  Test Generation Agent
       │                         │
       │                         ▼
       │                   Test Files (TS)
       │                         │
       │                         ▼
       │                   Playwright Runner
       │                         │
       │                         ▼
       │                Test Results + Logs
       │                         │
       │                         ▼
       │                   Log Parser
       │                         │
       │        ┌────────────────┴────────────────┐
       │        │                                  │
       ▼        ▼                                  │
QAResult   If Failures ──► RCA Agent ──┐         │
(Success)                     │         │         │
                              ▼         │         │
                          RCA Result    │         │
                                        │         │
                              ┌─────────┴────────┘
                              ▼
                          QAResult (With RCA)
```

## LLM Integration

### OpenAI Configuration
- **Model**: GPT-4o (default)
- **Temperature**: 0.1 (low randomness for consistency)
- **Timeout**: Inferred from OpenAI limits
- **Retries**: 3 attempts per operation

### Prompt Strategy
Each agent uses optimized prompts:
- **TestPlanAgent**: Detailed requirements for comprehensive test coverage
- **TestGenerationAgent**: Playwright best practices and patterns
- **RCAAgent**: Step-by-step analysis methodology

### Output Validation
All LLM outputs are validated with Pydantic models before use.

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Required for all LLM operations
- `PLAYWRIGHT_TIMEOUT`: Test execution timeout (ms)
- `LOG_LEVEL`: Logging verbosity
- `MAX_RETRIES`: Retry attempts for agents

### File Paths
- **Generated Tests**: `playwright-tests/tests/generated/`
- **Logs**: `logs/autonomous-qa.log`
- **Database**: `data/chromadb/`

## Extensibility

### Adding Custom Agents
1. Create new agent class inheriting from base pattern
2. Implement `__init__` with LLM setup
3. Implement main method with retry logic
4. Add to orchestrator workflow

### Adding Custom Tools
1. Create tool class in `tools/`
2. Implement required methods
3. Add exception handling
4. Integrate into workflow

## Security

- **API Keys**: Stored in `.env` (never committed)
- **LLM Inputs**: Sanitized before sending to OpenAI
- **File Operations**: Path traversal protected
- **Subprocess**: Timeouts prevent hangs
- **Logging**: Sensitive data excluded from logs

## Performance Considerations

- **Parallel Execution**: Tests run sequentially for now, can be parallelized
- **LLM Caching**: Consider caching for identical features
- **Log Parsing**: Regex patterns optimized for speed
- **Memory**: Results stored in memory (consider DB for large jobs)
