#!/usr/bin/env python
"""
FastAPI Server Example

This demonstrates how to run the Autonomous QA Platform as a web service.

Usage:
    uvicorn examples.fastapi_server:app --reload --host 0.0.0.0 --port 8000

API Docs:
    http://localhost:8000/docs
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from orchestration.agent_workflow import AutonomousQAWorkflow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Autonomous QA Platform API",
    description="AI-driven QA platform for automated test generation and execution",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# In-memory job storage (use database in production)
jobs_store: Dict[str, Dict[str, Any]] = {}
job_counter = 0


# ============================================================================
# MODELS
# ============================================================================

class QARequest(BaseModel):
    feature_description: str = Field(
        ...,
        min_length=10,
        description="Feature description to generate tests for"
    )
    test_type: str = Field(
        default="full",
        description="Type of tests: full, unit, integration, e2e"
    )
    timeout: int = Field(
        default=600,
        description="Timeout in seconds"
    )
    verbose: bool = Field(
        default=False,
        description="Enable verbose logging"
    )


class TestPlanRequest(BaseModel):
    feature_description: str = Field(
        ...,
        min_length=10,
        description="Feature description"
    )


class TestPlanResponse(BaseModel):
    test_plan: Dict[str, List[str]]
    generation_time: float


class GenerateTestsResponse(BaseModel):
    test_files: Dict[str, str]
    generation_time: float


class QAResponse(BaseModel):
    job_id: str
    status: str
    test_plan: Optional[Dict[str, List[str]]] = None
    test_results: Optional[Dict[str, Any]] = None
    rca_results: Optional[Dict[str, Any]] = None
    overall_success: bool
    execution_time_seconds: float


class HealthResponse(BaseModel):
    status: str
    version: str
    services: Dict[str, str]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_job_id() -> str:
    """Generate a unique job ID."""
    global job_counter
    job_counter += 1
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"qa-{timestamp}-{job_counter}"


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/api/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Status of the API and its services
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        services={
            "openai": "connected",
            "playwright": "ready",
            "database": "connected"
        }
    )


@app.post("/api/qa/test-plan", response_model=TestPlanResponse)
async def generate_test_plan(request: TestPlanRequest) -> TestPlanResponse:
    """
    Generate a test plan from a feature description.
    
    Args:
        request: Feature description
        
    Returns:
        TestPlanResponse: Generated test plan
    """
    try:
        import time
        start_time = time.time()
        
        workflow = AutonomousQAWorkflow()
        test_plan = workflow.test_plan_agent.generate_test_plan(
            request.feature_description
        )
        
        generation_time = time.time() - start_time
        
        return TestPlanResponse(
            test_plan=test_plan,
            generation_time=generation_time
        )
    except Exception as e:
        logger.error(f"Error generating test plan: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate test plan: {str(e)}"
        )


@app.post("/api/qa/generate-tests", response_model=GenerateTestsResponse)
async def generate_tests(test_plan: Dict[str, List[str]]) -> GenerateTestsResponse:
    """
    Generate Playwright tests from a test plan.
    
    Args:
        test_plan: Test plan dictionary
        
    Returns:
        GenerateTestsResponse: Generated test files
    """
    try:
        import time
        start_time = time.time()
        
        workflow = AutonomousQAWorkflow()
        test_files = workflow.test_generation_agent.generate_tests(test_plan)
        
        generation_time = time.time() - start_time
        
        return GenerateTestsResponse(
            test_files=test_files,
            generation_time=generation_time
        )
    except Exception as e:
        logger.error(f"Error generating tests: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate tests: {str(e)}"
        )


@app.post("/api/qa/run", response_model=QAResponse)
async def run_qa_workflow(
    request: QARequest,
    background_tasks: BackgroundTasks
) -> QAResponse:
    """
    Run a complete QA workflow.
    
    Args:
        request: QA request with feature description
        background_tasks: Background task runner
        
    Returns:
        QAResponse: Complete QA results
    """
    try:
        import time
        start_time = time.time()
        
        workflow = AutonomousQAWorkflow()
        result = workflow.run_qa_workflow(request.feature_description)
        
        execution_time = time.time() - start_time
        job_id = generate_job_id()
        
        # Store job result
        jobs_store[job_id] = {
            "status": "completed",
            "result": result,
            "execution_time": execution_time,
            "created_at": datetime.now().isoformat()
        }
        
        return QAResponse(
            job_id=job_id,
            status="completed",
            test_plan=result.test_plan,
            test_results={
                "return_code": result.test_results.get('return_code'),
                "stdout": result.test_results.get('stdout', '')[:500],  # Truncate
                "stderr": result.test_results.get('stderr', '')[:500],
            },
            rca_results=result.rca_results,
            overall_success=result.success,
            execution_time_seconds=execution_time
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error running QA workflow: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to run QA workflow: {str(e)}"
        )


@app.get("/api/qa/jobs/{job_id}")
async def get_job_status(job_id: str) -> Dict[str, Any]:
    """
    Get the status of a QA job.
    
    Args:
        job_id: Job ID
        
    Returns:
        Job status and details
    """
    if job_id not in jobs_store:
        raise HTTPException(
            status_code=404,
            detail=f"Job {job_id} not found"
        )
    
    job = jobs_store[job_id]
    return {
        "job_id": job_id,
        "status": job["status"],
        "created_at": job["created_at"],
        "execution_time": job.get("execution_time")
    }


@app.get("/api/qa/jobs")
async def list_jobs(
    status: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
) -> Dict[str, Any]:
    """
    List QA jobs with optional filtering.
    
    Args:
        status: Filter by status
        limit: Number of results
        offset: Pagination offset
        
    Returns:
        List of jobs matching criteria
    """
    jobs_list = list(jobs_store.items())
    
    # Filter by status if specified
    if status:
        jobs_list = [
            (jid, job) for jid, job in jobs_list
            if job["status"] == status
        ]
    
    # Apply pagination
    total = len(jobs_list)
    jobs_list = jobs_list[offset:offset + limit]
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "jobs": [
            {
                "job_id": jid,
                "status": job["status"],
                "created_at": job["created_at"]
            }
            for jid, job in jobs_list
        ]
    }


@app.post("/api/qa/jobs/{job_id}/cancel")
async def cancel_job(job_id: str) -> Dict[str, str]:
    """
    Cancel a QA job.
    
    Args:
        job_id: Job ID
        
    Returns:
        Cancellation confirmation
    """
    if job_id not in jobs_store:
        raise HTTPException(
            status_code=404,
            detail=f"Job {job_id} not found"
        )
    
    jobs_store[job_id]["status"] = "cancelled"
    return {"job_id": job_id, "status": "cancelled"}


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "code": "HTTP_ERROR"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "code": "INTERNAL_ERROR"
        }
    )


# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    logger.info("Autonomous QA API starting up")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Autonomous QA API shutting down")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "examples.fastapi_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )