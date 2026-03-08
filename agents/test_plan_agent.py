import os
import json
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestPlan(BaseModel):
    functional_tests: List[str] = Field(description="List of functional test scenarios")
    edge_cases: List[str] = Field(description="List of edge case test scenarios")
    api_tests: List[str] = Field(description="List of API test scenarios")
    ui_tests: List[str] = Field(description="List of UI test scenarios")

class TestPlanAgent:
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0.1, max_retries: int = 3):
        self.model_name = model_name
        self.temperature = temperature
        self.max_retries = max_retries
        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.parser = JsonOutputParser(pydantic_object=TestPlan)
        self.prompt = PromptTemplate(
            template="""
You are an expert QA engineer. Given a feature description, generate a comprehensive test plan.

Feature Description:
{feature_description}

Generate a structured test plan in JSON format with the following keys:
- functional_tests: List of functional test scenarios that cover the main functionality
- edge_cases: List of edge case scenarios that test boundaries and unusual conditions
- api_tests: List of API test scenarios if applicable
- ui_tests: List of UI test scenarios for user interface interactions

Each list should contain descriptive strings of test scenarios.

Ensure the test plan is thorough and covers all aspects of the feature.

{format_instructions}
""",
            input_variables=["feature_description"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )
        self.chain = self.prompt | self.llm | self.parser

    def generate_test_plan(self, feature_description: str) -> Dict[str, Any]:
        """
        Generate a test plan from feature description with retry logic.
        """
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Generating test plan, attempt {attempt + 1}")
                result = self.chain.invoke({"feature_description": feature_description})
                # Validate the result
                test_plan = TestPlan(**result)
                logger.info("Test plan generated successfully")
                return test_plan.model_dump()
            except Exception as e:
                logger.error(f"Error generating test plan on attempt {attempt + 1}: {e}")
                if attempt == self.max_retries - 1:
                    raise e
        return {}