from __future__ import annotations

from typing_extensions import TypedDict
from typing import List, Dict, Optional, Any


class Defect(TypedDict, total=False):
    severity: str  # Critical/High/Medium/Low
    title: str
    description: str
    suggestion: str


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

    # Control
    loop_count: int
    max_loops: int
    last_error: Optional[str]
    run_dir: Optional[str]
