import os
import json
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestGenerationAgent:
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0.1, max_retries: int = 3):
        self.model_name = model_name
        self.temperature = temperature
        self.max_retries = max_retries
        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.parser = StrOutputParser()
        self.prompt = PromptTemplate(
            template="""
You are an expert in Playwright test automation. Given a test plan JSON, generate Playwright TypeScript test files.

Test Plan:
{test_plan}

Generate Playwright test code for each category. Create separate test files for:
- Functional tests
- Edge case tests
- API tests
- UI tests

Each test file should be a complete Playwright test file with proper imports, test suites, and assertions.

For UI tests, use page objects and realistic selectors.
For API tests, use Playwright's API testing capabilities.
Include proper error handling and assertions.

Output the test code as a JSON object with keys: 'functional_tests.ts', 'edge_cases.ts', 'api_tests.ts', 'ui_tests.ts'

Each value should be the full content of the TypeScript file.
""",
            input_variables=["test_plan"],
        )
        self.chain = self.prompt | self.llm | self.parser

    def generate_tests(self, test_plan: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate Playwright test files from test plan with retry logic.
        """
        test_plan_str = json.dumps(test_plan, indent=2)
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Generating tests, attempt {attempt + 1}")
                result = self.chain.invoke({"test_plan": test_plan_str})
                # Parse the JSON output
                test_files = json.loads(result)
                logger.info("Tests generated successfully")
                return test_files
            except Exception as e:
                logger.error(f"Error generating tests on attempt {attempt + 1}: {e}")
                if attempt == self.max_retries - 1:
                    raise e
        return {}