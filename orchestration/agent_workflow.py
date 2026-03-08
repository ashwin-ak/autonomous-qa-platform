"""
PROJECT: Autonomous QA Platform

Build a Python-based AI-driven Autonomous QA system.
...
"""

import os
import json
import logging
from typing import Dict, Any, List
from agents.test_plan_agent import TestPlanAgent
from agents.test_generation_agent import TestGenerationAgent
from agents.rca_agent import RCAAgent
from tools.playwright_runner import PlaywrightRunner
from tools.log_parser import LogParser

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QAResult:
    def __init__(self, test_plan: Dict, test_results: Dict, rca_results: Dict = None):
        self.test_plan = test_plan
        self.test_results = test_results
        self.rca_results = rca_results
        self.success = test_results.get('return_code', -1) == 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_plan": self.test_plan,
            "test_results": self.test_results,
            "rca_results": self.rca_results,
            "overall_success": self.success
        }

class AutonomousQAWorkflow:
    def __init__(self):
        self.test_plan_agent = TestPlanAgent()
        self.test_generation_agent = TestGenerationAgent()
        self.rca_agent = RCAAgent()
        self.playwright_runner = PlaywrightRunner()
        self.log_parser = LogParser()

    def run_qa_workflow(self, feature_description: str) -> QAResult:
        """
        Main QA workflow orchestration.
        """
        try:
            logger.info("Starting QA workflow")

            # Step 1: Generate test plan
            logger.info("Generating test plan")
            test_plan = self.test_plan_agent.generate_test_plan(feature_description)

            # Step 2: Generate test code
            logger.info("Generating test code")
            test_files = self.test_generation_agent.generate_tests(test_plan)

            # Write test files to playwright-tests/tests/generated
            self._write_test_files(test_files)

            # Step 3: Execute tests
            logger.info("Executing Playwright tests")
            stdout, stderr, return_code = self.playwright_runner.run_tests()

            test_results = {
                "stdout": stdout,
                "stderr": stderr,
                "return_code": return_code,
                "parsed_logs": self.log_parser.format_logs_for_ai(stdout, stderr)
            }

            # Step 4: If failures, perform RCA
            rca_results = None
            if return_code != 0:
                logger.info("Tests failed, performing root cause analysis")
                failures = test_results["parsed_logs"]["errors"]
                logs = test_results["parsed_logs"]["full_logs"]
                stack_traces = "\n".join(test_results["parsed_logs"]["stack_traces"])
                rca_results = self.rca_agent.analyze_failures(failures, logs, stack_traces)

            logger.info("QA workflow completed")
            return QAResult(test_plan, test_results, rca_results)

        except Exception as e:
            logger.error(f"Error in QA workflow: {e}")
            raise

    def _write_test_files(self, test_files: Dict[str, str]):
        """
        Write generated test files to the test directory.
        """
        base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "playwright-tests", "tests", "generated")
        os.makedirs(base_dir, exist_ok=True)

        for filename, content in test_files.items():
            filepath = os.path.join(base_dir, filename)
            with open(filepath, 'w') as f:
                f.write(content)
            logger.info(f"Written test file: {filepath}")

# Example usage
if __name__ == "__main__":
    workflow = AutonomousQAWorkflow()
    feature_desc = "Implement a login feature with email and password validation"
    result = workflow.run_qa_workflow(feature_desc)
    print(json.dumps(result.to_dict(), indent=2))