# Configuration Guide

**Author:** Ashwin Kulkarni  
**License:** MIT

## Environment Variables

Create a `.env` file in the root directory (copy from `.env.example`):

```bash
cp .env.example .env
```

### Required Variables

#### OpenAI Configuration
```env
OPENAI_API_KEY=sk-...                # Your OpenAI API key (required)
OPENAI_MODEL=gpt-4o                  # Model to use (default: gpt-4o)
```

**Getting your API key**:
1. Go to [platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
2. Create a new API key
3. Copy and paste into `.env`

### Optional Variables

#### Playwright Configuration
```env
PLAYWRIGHT_TIMEOUT=30000             # Default timeout in milliseconds
PLAYWRIGHT_HEADLESS=true             # Run in headless mode
PLAYWRIGHT_BROWSER=chromium          # Browser to use (chromium, firefox, webkit)
```

#### Logging
```env
LOG_LEVEL=INFO                       # Log level (DEBUG, INFO, WARNING, ERROR)
LOG_FILE=logs/autonomous-qa.log      # Log file path
```

#### Agent Configuration
```env
MAX_RETRIES=3                        # Retries for agent operations
TEST_GRID_SIZE=4                     # Concurrent test execution
```

#### Database
```env
CHROMADB_PATH=./data/chromadb        # ChromaDB storage path
PERSIST_DIRECTORY=./data/persist     # Persistence directory
```

## Configuration File

Optionally, use `config/config.yaml` for YAML-based configuration:

```yaml
openai:
  api_key: ${OPENAI_API_KEY}
  model: gpt-4o
  temperature: 0.1
  max_retries: 3

playwright:
  timeout: 30000
  headless: true
  browser: chromium
  
logging:
  level: INFO
  file: logs/autonomous-qa.log
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

test_execution:
  grid_size: 4
  max_duration: 3600
  
database:
  chromadb_path: ./data/chromadb
  persist_dir: ./data/persist
```

## Loading Configuration

### From Environment Variables
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
```

### From Config File
```python
import yaml

with open('config/config.yaml') as f:
    config = yaml.safe_load(f)
    api_key = config['openai']['api_key']
```

### Programmatic Configuration
```python
from agents.test_plan_agent import TestPlanAgent

agent = TestPlanAgent(
    model_name="gpt-4o",
    temperature=0.1,
    max_retries=3
)
```

## LLM Settings

### Model Selection
- **gpt-4o**: Default, best quality (recommended)
- **gpt-4**: Older version, still capable
- **gpt-3.5-turbo**: Faster, lower cost (less reliable)

### Temperature Settings
- **0.0**: Deterministic, consistent results
- **0.1**: Low randomness (recommended for QA)
- **0.5**: Balanced
- **1.0**: Maximum randomness/creativity

### Timeout Configuration
Each configuration level can specify timeouts:

```python
# Agent timeout
agent = TestPlanAgent(timeout=60)  # 60 seconds

# LLM timeout
llm = ChatOpenAI(timeout=30)  # 30 seconds

# Test execution timeout
runner = PlaywrightRunner(timeout=300)  # 5 minutes
```

## Folder Structure

Create these directories for proper organization:

```bash
# Logs directory
mkdir -p logs

# Data directories
mkdir -p data/chromadb
mkdir -p data/persist

# Configuration
mkdir -p config

# Test outputs
mkdir -p playwright-tests/tests/generated
mkdir -p playwright-tests/reports
```

## Database Configuration

### ChromaDB Setup
```python
import chromadb

# In-memory (default)
client = chromadb.Client()

# Persistent
client = chromadb.PersistentClient(
    path="./data/chromadb"
)

# Create collection
collection = client.get_or_create_collection(name="qa_tests")
```

## API Server Configuration

### FastAPI Settings
```python
from fastapi import FastAPI

app = FastAPI(
    title="Autonomous QA API",
    version="1.0.0",
    docs_url="/api/docs"
)

# CORS settings
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Production Deployment

### Security Checklist
- [ ] Use strong API keys
- [ ] Never commit `.env` to version control
- [ ] Use environment-specific configs
- [ ] Enable CORS restrictions
- [ ] Set up proper logging
- [ ] Configure rate limiting
- [ ] Use HTTPS only
- [ ] Implement authentication

### Production Configuration
```yaml
openai:
  model: gpt-4o
  max_retries: 3
  timeout: 60

playwright:
  timeout: 30000
  headless: true
  browser: chromium

logging:
  level: WARNING
  file: logs/qa-prod.log

database:
  chromadb_path: /var/lib/qa/chromadb
```

## Troubleshooting

### API Key Issues
```
Error: Invalid API key
→ Check OPENAI_API_KEY in .env
→ Verify key is active on OpenAI dashboard
→ Ensure no extra spaces in key
```

### Playwright Issues
```
Error: Playwright browsers not found
→ Run: playwright install
→ Check PLAYWRIGHT_BROWSER setting
```

### Timeout Issues
```
Error: Operation timed out
→ Increase PLAYWRIGHT_TIMEOUT
→ Increase agent timeout settings
→ Check system resources
```

### Memory Issues
```
Error: Out of memory
→ Increase system RAM
→ Reduce TEST_GRID_SIZE
→ Enable ChromaDB persistence
```