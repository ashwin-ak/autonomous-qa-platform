#!/usr/bin/env python
"""
Basic Workflow Example

This demonstrates how to use the Autonomous QA Platform
to run a complete QA workflow on a feature description.
"""

import json
import logging
from orchestration.agent_workflow import AutonomousQAWorkflow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Run a basic QA workflow."""
    
    # Initialize the workflow
    logger.info("Initializing Autonomous QA Workflow")
    workflow = AutonomousQAWorkflow()
    
    # Feature description to test
    feature_description = """
    Implement a user login feature with the following requirements:
    
    1. Email and password validation
    2. Remember me functionality (30 days)
    3. Password reset via email link
    4. Account lockout after 5 failed login attempts
    5. Password strength requirements:
       - Minimum 8 characters
       - At least one uppercase letter
       - At least one number
       - At least one special character
    6. Session management with JWT tokens
    7. Rate limiting on login endpoint
    """
    
    try:
        # Run the workflow
        logger.info("Starting QA workflow execution")
        result = workflow.run_qa_workflow(feature_description)
        
        # Display results
        logger.info("QA workflow completed successfully")
        
        print("\n" + "="*80)
        print("QA WORKFLOW RESULTS")
        print("="*80)
        
        # Test Plan
        print("\n[TEST PLAN]")
        print(json.dumps(result.test_plan, indent=2))
        
        # Test Results
        print("\n[TEST RESULTS]")
        test_results = {
            "return_code": result.test_results.get('return_code'),
            "overall_success": result.success
        }
        if 'parsed_logs' in result.test_results:
            test_results['error_count'] = len(
                result.test_results['parsed_logs'].get('errors', [])
            )
        print(json.dumps(test_results, indent=2))
        
        # RCA Results (if failures occurred)
        if result.rca_results:
            print("\n[ROOT CAUSE ANALYSIS]")
            print(json.dumps(result.rca_results, indent=2))
        
        # Summary
        print("\n" + "="*80)
        if result.success:
            print("✓ All tests passed!")
        else:
            print("✗ Some tests failed. See RCA above for details.")
        print("="*80)
        
        return 0 if result.success else 1
        
    except Exception as e:
        logger.error(f"Error running workflow: {e}", exc_info=True)
        print(f"\n✗ Workflow failed with error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())