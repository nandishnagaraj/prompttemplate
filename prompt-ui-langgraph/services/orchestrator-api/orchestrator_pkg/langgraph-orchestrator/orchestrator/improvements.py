"""
Improvements module: Structured defect extraction, async parallelization, error tracking, logging.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
import re
from typing import Any, List, Callable, Optional, Dict, TypeVar
from datetime import datetime

from .state import Defect, NodeMetrics, TokenMetrics

# Configure structured logging
logger = logging.getLogger("orchestrator")


class StructuredLogger:
    """Helper for adding structured logs to orchestrator state."""
    
    def __init__(self, state: Dict[str, Any]):
        self.state = state
        if "execution_log" not in state:
            state["execution_log"] = []
    
    def log(self, level: str, message: str, **context):
        """Add structured log entry."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            **context,
        }
        self.state["execution_log"].append(entry)
        logger.log(getattr(logging, level, logging.INFO), f"{message} | {json.dumps(context)}")
    
    def info(self, message: str, **context):
        self.log("INFO", message, **context)
    
    def warning(self, message: str, **context):
        self.log("WARNING", message, **context)
    
    def error(self, message: str, **context):
        self.log("ERROR", message, **context)


def extract_defects_json(coverage_gaps: str, llm: Any) -> List[Defect]:
    """
    Extract defects from coverage_gaps using JSON parsing.
    
    Attempts to parse JSON block from LLM output; falls back to regex if JSON not found.
    """
    defects: List[Defect] = []
    
    # Try JSON parsing first
    json_pattern = r'```json\s*\n?(.*?)\n?```'
    json_match = re.search(json_pattern, coverage_gaps, re.DOTALL)
    
    if json_match:
        try:
            json_str = json_match.group(1)
            data = json.loads(json_str)
            if isinstance(data, dict) and "defects" in data:
                for defect_obj in data.get("defects", []):
                    if isinstance(defect_obj, dict):
                        defects.append({
                            "severity": defect_obj.get("severity", "Medium"),
                            "title": defect_obj.get("title", "Unknown"),
                            "description": defect_obj.get("description", ""),
                            "suggestion": defect_obj.get("suggestion", ""),
                        })
                if defects:
                    return defects
        except json.JSONDecodeError:
            pass
    
    # Fallback: regex extraction
    pattern = re.compile(
        r"\[(?:SEVERITY|Severity):\s*(Critical|High|Medium|Low)\]\s*[-—]\s*(.*?)(?:\n|$)",
        re.MULTILINE
    )
    for match in pattern.finditer(coverage_gaps):
        defects.append({
            "severity": match.group(1),
            "title": match.group(2).strip(),
            "description": match.group(0).strip(),
            "suggestion": "",
        })
    
    return defects


def track_node_execution(node_name: str):
    """Decorator to track node execution metrics and errors."""
    def decorator(func: Callable) -> Callable:
        async def async_wrapper(state: Dict[str, Any], **kwargs) -> Dict[str, Any]:
            start_time = time.time()
            logger_instance = StructuredLogger(state)
            
            try:
                logger_instance.info(f"Starting {node_name}", node=node_name)
                result = await func(state, **kwargs) if asyncio.iscoroutinefunction(func) else func(state, **kwargs)
                
                execution_time_ms = (time.time() - start_time) * 1000
                logger_instance.info(
                    f"Completed {node_name}",
                    node=node_name,
                    execution_time_ms=execution_time_ms
                )
                
                # Track metrics
                if "node_metrics" not in result:
                    result["node_metrics"] = {}
                
                result["node_metrics"][node_name] = {
                    "execution_time_ms": execution_time_ms,
                    "artifacts_generated": [],  # Can be populated by node
                }
                
                return result
            except Exception as e:
                execution_time_ms = (time.time() - start_time) * 1000
                logger_instance.error(
                    f"Error in {node_name}: {str(e)}",
                    node=node_name,
                    error=str(e),
                    execution_time_ms=execution_time_ms
                )
                state["last_error"] = f"{node_name}: {str(e)}"
                if "node_metrics" not in state:
                    state["node_metrics"] = {}
                state["node_metrics"][node_name] = {
                    "execution_time_ms": execution_time_ms,
                    "error": str(e),
                    "artifacts_generated": [],
                }
                raise
        
        def sync_wrapper(state: Dict[str, Any], **kwargs) -> Dict[str, Any]:
            start_time = time.time()
            logger_instance = StructuredLogger(state)
            
            try:
                logger_instance.info(f"Starting {node_name}", node=node_name)
                result = func(state, **kwargs)
                
                execution_time_ms = (time.time() - start_time) * 1000
                logger_instance.info(
                    f"Completed {node_name}",
                    node=node_name,
                    execution_time_ms=execution_time_ms
                )
                
                if "node_metrics" not in result:
                    result["node_metrics"] = {}
                result["node_metrics"][node_name] = {
                    "execution_time_ms": execution_time_ms,
                    "artifacts_generated": [],
                }
                
                return result
            except Exception as e:
                execution_time_ms = (time.time() - start_time) * 1000
                logger_instance.error(
                    f"Error in {node_name}: {str(e)}",
                    node=node_name,
                    error=str(e),
                    execution_time_ms=execution_time_ms
                )
                state["last_error"] = f"{node_name}: {str(e)}"
                if "node_metrics" not in state:
                    state["node_metrics"] = {}
                state["node_metrics"][node_name] = {
                    "execution_time_ms": execution_time_ms,
                    "error": str(e),
                }
                raise
        
        return sync_wrapper
    return decorator


def parallel_invoke(llm: Any, prompts: List[tuple[str, str]]) -> List[str]:
    """
    Invoke LLM on multiple prompts concurrently using threading pool.
    
    Args:
        llm: LLM instance with invoke method
        prompts: List of (prompt_name, prompt_text) tuples
    
    Returns:
        List of outputs in same order as prompts
    """
    from concurrent.futures import ThreadPoolExecutor
    
    def invoke_one(prompt_text: str) -> str:
        return llm.invoke(prompt_text)
    
    results = []
    with ThreadPoolExecutor(max_workers=min(3, len(prompts))) as executor:
        futures = [executor.submit(invoke_one, prompt_text) for _, prompt_text in prompts]
        results = [future.result() for future in futures]
    
    return results


def check_cost_limits(state: Dict[str, Any], llm: Any) -> bool:
    """
    Check if token or cost limits have been exceeded.
    
    Returns:
        True if limits respected, False if limit exceeded
    """
    max_tokens = state.get("max_tokens", 1_000_000)
    cost_limit = state.get("cost_limit_usd", float("inf"))
    
    if hasattr(llm, "token_usage"):
        total_tokens = llm.token_usage.get("total_tokens", 0)
        total_cost = llm.token_usage.get("estimated_cost_usd", 0)
        
        if total_tokens > max_tokens:
            return False
        if total_cost > cost_limit:
            return False
    
    return True


def update_token_metrics(state: Dict[str, Any], llm: Any):
    """Update state with current token metrics from LLM."""
    if hasattr(llm, "token_usage"):
        state["total_token_metrics"] = {
            "prompt_tokens": llm.token_usage.get("prompt_tokens", 0),
            "completion_tokens": llm.token_usage.get("completion_tokens", 0),
            "total_tokens": llm.token_usage.get("total_tokens", 0),
            "estimated_cost_usd": llm.token_usage.get("estimated_cost_usd", 0),
        }
