import os
import json
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RCAResult(BaseModel):
    root_cause: str = Field(description="The root cause of the failure")
    suspected_module: str = Field(description="The suspected module or component causing the issue")
    suggested_fix: str = Field(description="Suggested fix for the issue")
    confidence_score: float = Field(description="Confidence score between 0 and 1")

class RCAAgent:
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0.1, max_retries: int = 3):
        self.model_name = model_name
        self.temperature = temperature
        self.max_retries = max_retries
        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.parser = JsonOutputParser(pydantic_object=RCAResult)
        self.prompt = PromptTemplate(
            template="""
You are an expert in root cause analysis for software failures. Analyze the provided test failures, logs, and stack traces.

Test Failures:
{test_failures}

Logs:
{logs}

Stack Traces:
{stack_traces}

Perform root cause analysis and provide:
- root_cause: A detailed explanation of the root cause
- suspected_module: The suspected module or component
- suggested_fix: A suggested fix
- confidence_score: A confidence score between 0 and 1

{format_instructions}
""",
            input_variables=["test_failures", "logs", "stack_traces"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )
        self.chain = self.prompt | self.llm | self.parser

    def analyze_failures(self, test_failures: List[str], logs: str, stack_traces: str) -> Dict[str, Any]:
        """
        Analyze failures and return RCA with retry logic.
        """
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Analyzing failures, attempt {attempt + 1}")
                result = self.chain.invoke({
                    "test_failures": "\n".join(test_failures),
                    "logs": logs,
                    "stack_traces": stack_traces
                })
                rca = RCAResult(**result)
                logger.info("RCA completed successfully")
                return rca.model_dump()
            except Exception as e:
                logger.error(f"Error in RCA on attempt {attempt + 1}: {e}")
                if attempt == self.max_retries - 1:
                    raise e
        return {}