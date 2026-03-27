from __future__ import annotations

from typing_extensions import TypedDict
from typing import List, Dict, Optional, Any


class Defect(TypedDict, total=False):
    severity: str  # Critical/High/Medium/Low
    title: str
    description: str
    suggestion: str


class TokenMetrics(TypedDict, total=False):
    """Token usage metrics per artifact or node."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost_usd: float


class NodeMetrics(TypedDict, total=False):
    """Execution metrics per node."""
    tokens: TokenMetrics
    error: Optional[str]
    execution_time_ms: float
    artifacts_generated: List[str]


class OrchestratorState(TypedDict, total=False):
    # Inputs
    idea: str
    tech_stack: str

    # PM artifacts
    prd: str
    use_cases: str
    rtm: str
    pm_open_questions: List[str]

    # Architect artifacts
    architecture: str
    adrs: str
    api_contract: str
    arch_risks: str

    # Dev artifacts
    user_stories: str
    implementation_plan: str
    code_skeleton: str
    dev_notes: str

    # QA artifacts
    test_plan: str
    defect_list: List[Defect]
    coverage_map: str

    # Control & Limits
    loop_count: int
    max_loops: int
    max_tokens: int  # Safety limit per run
    cost_limit_usd: float  # Safety limit on total cost
    last_error: Optional[str]
    run_dir: Optional[str]
    
    # Metrics & Observability
    total_token_metrics: TokenMetrics
    node_metrics: Dict[str, NodeMetrics]  # per-node execution stats
    execution_log: List[str]  # structured execution trace
