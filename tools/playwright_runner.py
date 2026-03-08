import subprocess
import os
import logging
from typing import Tuple

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlaywrightRunner:
    def __init__(self, test_dir: str = "playwright-tests"):
        self.test_dir = test_dir
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def run_tests(self, test_files: list = None) -> Tuple[str, str, int]:
        """
        Run Playwright tests and return stdout, stderr, and return code.
        """
        try:
            cmd = ["npx", "playwright", "test"]
            if test_files:
                cmd.extend(test_files)
            else:
                cmd.append("--grep", "generated")  # Assuming generated tests have this in name

            # Change to test directory
            cwd = os.path.join(self.project_root, self.test_dir)

            logger.info(f"Running command: {' '.join(cmd)} in {cwd}")
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )

            stdout = result.stdout
            stderr = result.stderr
            return_code = result.returncode

            logger.info(f"Tests completed with return code: {return_code}")
            return stdout, stderr, return_code

        except subprocess.TimeoutExpired:
            logger.error("Playwright tests timed out")
            return "", "Timeout expired", -1
        except Exception as e:
            logger.error(f"Error running Playwright tests: {e}")
            return "", str(e), -1