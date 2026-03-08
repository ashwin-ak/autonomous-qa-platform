# API Reference

**Author:** Ashwin Kulkarni  
**Email:** ashwin.ak21@gmail.com  
**License:** MIT

## Overview

The Autonomous QA Platform provides a REST API for programmatic access to QA workflows.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. In production, implement OAuth2 or API key authentication.

## Endpoints

### 1. Run QA Workflow

Run a complete QA workflow on a feature description.

**Endpoint**: `POST /api/qa/run`

**Request Body**:
```json
{
  "feature_description": "User login feature with email/password validation",
  "test_type": "full",  // "full", "unit", "integration", "e2e"
  "timeout": 600,  // seconds
  "verbose": true
}
```

**Response (200 OK)**:
```json
{
  "job_id": "qa-20240308-123456",
  "status": "completed",
  "test_plan": {
    "functional_tests": ["Test login with valid credentials", "Test logout"],
    "edge_cases": ["Empty email field", "Very long password"],
    "api_tests": ["POST /api/auth/login", "GET /api/auth/me"],
    "ui_tests": ["Login form visibility", "Error message display"]
  },
  "test_results": {
    "return_code": 0,
    "stdout": "...",
    "stderr": "",
    "total_tests": 8,
    "passed": 8,
    "failed": 0
  },
  "rca_results": null,
  "overall_success": true,
  "execution_time_seconds": 45.23
}
```

**Response (400 Bad Request)**:
```json
{
  "error": "Feature description cannot be empty",
  "code": "INVALID_INPUT"
}
```

**Response (500 Internal Server Error)**:
```json
{
  "error": "OpenAI API error: Rate limit exceeded",
  "code": "EXTERNAL_API_ERROR",
  "details": "..."
}
```

### 2. Get Test Plan

Generate only a test plan without executing tests.

**Endpoint**: `POST /api/qa/test-plan`

**Request Body**:
```json
{
  "feature_description": "User login feature"
}
```

**Response (200 OK)**:
```json
{
  "test_plan": {
    "functional_tests": ["Test login", "Test logout"],
    "edge_cases": ["Empty fields"],
    "api_tests": ["POST /auth/login"],
    "ui_tests": ["Form display"]
  }
}
```

### 3. Generate Tests

Generate Playwright tests from a test plan.

**Endpoint**: `POST /api/qa/generate-tests`

**Request Body**:
```json
{
  "test_plan": {
    "functional_tests": ["Test login", "Test logout"],
    "edge_cases": ["Empty fields"],
    "api_tests": ["POST /auth/login"],
    "ui_tests": ["Form display"]
  }
}
```

**Response (200 OK)**:
```json
{
  "test_files": {
    "functional_tests.ts": "import { test, expect } from '@playwright/test';\n...",
    "ui_tests.ts": "...",
    "api_tests.ts": "...",
    "edge_cases.ts": "..."
  }
}
```

### 4. Execute Tests

Execute previously generated or existing Playwright tests.

**Endpoint**: `POST /api/qa/execute-tests`

**Request Body**:
```json
{
  "test_files": ["functional_tests.ts", "ui_tests.ts"],
  "timeout": 300
}
```

**Response (200 OK)**:
```json
{
  "return_code": 0,
  "stdout": "...",
  "stderr": "",
  "total_tests": 5,
  "passed": 5,
  "failed": 0,
  "duration": 45
}
```

### 5. Analyze Failures

Perform root cause analysis on test failures.

**Endpoint**: `POST /api/qa/analyze-failures`

**Request Body**:
```json
{
  "test_failures": [
    "Login test failed: Element not found",
    "Password validation test failed: Timeout"
  ],
  "logs": "stderr output...",
  "stack_traces": "Error: timeout\n  at async page.click()"
}
```

**Response (200 OK)**:
```json
{
  "root_cause": "Missing wait condition on login button",
  "suspected_module": "LoginForm component",
  "suggested_fix": "Use page.waitForSelector() before clicking login button",
  "confidence_score": 0.92
}
```

### 6. Get Job Status

Get the status of a running QA job.

**Endpoint**: `GET /api/qa/jobs/{job_id}`

**Response (200 OK)**:
```json
{
  "job_id": "qa-20240308-123456",
  "status": "running",  // "queued", "running", "completed", "failed"
  "progress": 65,  // percentage
  "start_time": "2024-03-08T12:34:56Z",
  "estimated_completion": "2024-03-08T12:36:30Z"
}
```

### 7. List Jobs

List all QA jobs with optional filtering.

**Endpoint**: `GET /api/qa/jobs`

**Query Parameters**:
- `status`: Filter by status (running, completed, failed)
- `limit`: Number of results (default: 10, max: 100)
- `offset`: Pagination offset (default: 0)

**Response (200 OK)**:
```json
{
  "total": 42,
  "limit": 10,
  "offset": 0,
  "jobs": [
    {
      "job_id": "qa-20240308-123456",
      "status": "completed",
      "created_at": "2024-03-08T12:34:56Z",
      "completed_at": "2024-03-08T12:36:30Z"
    }
  ]
}
```

### 8. Cancel Job

Cancel a running QA job.

**Endpoint**: `POST /api/qa/jobs/{job_id}/cancel`

**Response (200 OK)**:
```json
{
  "job_id": "qa-20240308-123456",
  "status": "cancelled"
}
```

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| `INVALID_INPUT` | 400 | Request validation failed |
| `MISSING_REQUIRED_FIELD` | 400 | Missing required field |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMITED` | 429 | Too many requests |
| `EXTERNAL_API_ERROR` | 503 | OpenAI or Playwright error |
| `INTERNAL_ERROR` | 500 | Server error |

## Rate Limiting

- **Authenticated users**: 100 requests/hour
- **Anonymous users**: 10 requests/hour

## Webhooks

Configure webhooks to receive job completion notifications:

```bash
# Register webhook
POST /api/webhooks
{
  "url": "https://your-domain.com/webhook",
  "events": ["qa.completed", "qa.failed"]
}

# Webhook payload
{
  "event": "qa.completed",
  "job_id": "qa-20240308-123456",
  "timestamp": "2024-03-08T12:36:30Z",
  "data": { ... }
}
```

## SDKs

### Python SDK

```python
from autonomous_qa import QAClient

client = QAClient(base_url="http://localhost:8000")

result = client.run_qa_workflow(
    feature_description="User login feature"
)

print(f"Status: {result['overall_success']}")
```

### JavaScript/TypeScript SDK

```typescript
import { QAClient } from 'autonomous-qa-client';

const client = new QAClient({
  baseUrl: 'http://localhost:8000'
});

const result = await client.runQAWorkflow({
  featureDescription: 'User login feature'
});

console.log(`Status: ${result.overallSuccess}`);
```

## Examples

### Example 1: Full Workflow
```bash
curl -X POST http://localhost:8000/api/qa/run \
  -H "Content-Type: application/json" \
  -d '{
    "feature_description": "Implement user registration with email verification"
  }'
```

### Example 2: Test Plan Only
```bash
curl -X POST http://localhost:8000/api/qa/test-plan \
  -H "Content-Type: application/json" \
  -d '{
    "feature_description": "Add forgot password functionality"
  }'
```

### Example 3: Execute Tests
```bash
curl -X POST http://localhost:8000/api/qa/execute-tests \
  -H "Content-Type: application/json" \
  -d '{
    "test_files": ["tests/login.ts"],
    "timeout": 300
  }'
```

## Health Check

**Endpoint**: `GET /api/health`

**Response (200 OK)**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "openai": "connected",
    "playwright": "ready",
    "database": "connected"
  }
}
```

## Rate Limit Headers

All responses include rate limit information:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1709904600
```

## Versioning

Current API version: `v1`

Breaking changes will bump major version (e.g., `v2`). Use `Accept: application/vnd.qa.v1+json` header to specify version.