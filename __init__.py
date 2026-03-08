"""
Autonomous QA Platform

An AI-driven autonomous QA system that generates tests, executes them,
and performs root cause analysis using LLM agents.
"""

__version__ = "1.0.0"
__author__ = "Ashwin Kulkarni"

from orchestration.agent_workflow import AutonomousQAWorkflow, QAResult

__all__ = [
    "AutonomousQAWorkflow",
    "QAResult",
]