"""
Evaluation and metrics module for the Autonomous QA Platform.

This module provides functionality for evaluating agent performance,
tracking metrics, and analyzing test results.
"""

import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import json
import os
from config import get_config


@dataclass
class AgentMetrics:
    """Metrics for tracking agent performance."""
    agent_name: str
    operation: str
    start_time: float
    end_time: Optional[float] = None
    success: bool = False
    error_message: Optional[str] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

    @property
    def duration(self) -> Optional[float]:
        """Calculate duration in seconds."""
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        return None

    def complete(self, success: bool = True, error_message: Optional[str] = None):
        """Mark the operation as complete."""
        self.end_time = time.time()
        self.success = success
        if error_message:
            self.error_message = error_message


class MetricsCollector:
    """Collector for agent performance metrics."""

    def __init__(self):
        """Initialize the metrics collector."""
        self.metrics: List[AgentMetrics] = []
        self.config = get_config()

    def start_operation(self, agent_name: str, operation: str,
                       metadata: Optional[Dict[str, Any]] = None) -> AgentMetrics:
        """
        Start tracking a new operation.

        Args:
            agent_name: Name of the agent
            operation: Name of the operation
            metadata: Optional metadata

        Returns:
            AgentMetrics instance for tracking
        """
        metric = AgentMetrics(
            agent_name=agent_name,
            operation=operation,
            start_time=time.time(),
            metadata=metadata
        )
        self.metrics.append(metric)
        return metric

    def get_metrics_summary(self) -> Dict[str, Any]:
        """
        Get a summary of collected metrics.

        Returns:
            Dictionary with metrics summary
        """
        if not self.metrics:
            return {"total_operations": 0, "success_rate": 0.0}

        total_ops = len(self.metrics)
        successful_ops = len([m for m in self.metrics if m.success])
        avg_duration = sum(m.duration for m in self.metrics if m.duration) / total_ops

        return {
            "total_operations": total_ops,
            "successful_operations": successful_ops,
            "success_rate": successful_ops / total_ops if total_ops > 0 else 0.0,
            "average_duration": avg_duration,
            "operations_by_agent": self._group_by_agent()
        }

    def _group_by_agent(self) -> Dict[str, Dict[str, Any]]:
        """Group metrics by agent name."""
        agent_stats = {}
        for metric in self.metrics:
            if metric.agent_name not in agent_stats:
                agent_stats[metric.agent_name] = {
                    "total": 0,
                    "successful": 0,
                    "average_duration": 0.0
                }

            agent_stats[metric.agent_name]["total"] += 1
            if metric.success:
                agent_stats[metric.agent_name]["successful"] += 1

            if metric.duration:
                # Simple moving average
                current_avg = agent_stats[metric.agent_name]["average_duration"]
                count = agent_stats[metric.agent_name]["total"]
                agent_stats[metric.agent_name]["average_duration"] = (
                    (current_avg * (count - 1)) + metric.duration
                ) / count

        return agent_stats

    def save_metrics(self, filepath: Optional[str] = None):
        """
        Save metrics to a JSON file.

        Args:
            filepath: Optional path to save metrics (defaults to logs/metrics.json)
        """
        if not filepath:
            filepath = os.path.join("logs", "metrics.json")

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        data = {
            "timestamp": datetime.now().isoformat(),
            "summary": self.get_metrics_summary(),
            "metrics": [asdict(m) for m in self.metrics]
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def clear_metrics(self):
        """Clear all collected metrics."""
        self.metrics.clear()


# Global instance for easy access
metrics_collector = MetricsCollector()
