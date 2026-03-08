import re
import logging
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LogParser:
    def __init__(self):
        # Regex patterns for common error formats
        self.error_pattern = re.compile(r'ERROR|Error|error|FAIL|fail', re.IGNORECASE)
        self.stack_trace_pattern = re.compile(r'at\s+.*?\(.*?\)', re.MULTILINE)
        self.exception_pattern = re.compile(r'(Exception|Error):\s*(.*?)(?:\n|$)', re.IGNORECASE)

    def extract_errors(self, logs: str) -> List[str]:
        """
        Extract error messages from logs.
        """
        errors = []
        lines = logs.split('\n')
        for line in lines:
            if self.error_pattern.search(line):
                errors.append(line.strip())
        return errors

    def extract_stack_traces(self, logs: str) -> List[str]:
        """
        Extract stack traces from logs.
        """
        stack_traces = self.stack_trace_pattern.findall(logs)
        return stack_traces

    def extract_exceptions(self, logs: str) -> List[str]:
        """
        Extract exception messages.
        """
        exceptions = self.exception_pattern.findall(logs)
        return [f"{exc[0]}: {exc[1]}" for exc in exceptions]

    def format_logs_for_ai(self, stdout: str, stderr: str) -> Dict[str, Any]:
        """
        Format logs for AI agent consumption.
        """
        all_logs = stdout + "\n" + stderr

        formatted = {
            "errors": self.extract_errors(all_logs),
            "stack_traces": self.extract_stack_traces(all_logs),
            "exceptions": self.extract_exceptions(all_logs),
            "full_logs": all_logs
        }

        logger.info(f"Extracted {len(formatted['errors'])} errors, {len(formatted['stack_traces'])} stack traces")
        return formatted