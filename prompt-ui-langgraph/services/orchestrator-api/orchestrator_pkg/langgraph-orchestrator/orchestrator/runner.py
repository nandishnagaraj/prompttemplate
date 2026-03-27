from __future__ import annotations

"""Optional multi-iteration runner that explicitly re-invokes the graph while bumping loop_count.

This is useful if you want deterministic loop control in a simple script without checkpointers.
"""

from pathlib import Path
import json
from typing import Iterable, Set

from .llm import build_llm
from .io_utils import make_run_dir, write_artifact
from .nodes import pm_node, architect_node, developer_node, qa_node
from .prompts import PromptLibrary
from .improvements import update_token_metrics, check_cost_limits


ALL_ARTIFACTS = {
    "prd",
    "prd_gap_review",
    "use_cases",
    "rtm",
    "architecture",
    "api_contract",
    "arch_risks",
    "user_stories",
    "implementation_plan",
    "code_skeleton",
    "test_plan",
    "coverage_gaps",
}

ARTIFACT_NODE = {
    "prd": "pm",
    "prd_gap_review": "pm",
    "use_cases": "pm",
    "rtm": "pm",
    "architecture": "arch",
    "api_contract": "arch",
    "arch_risks": "arch",
    "user_stories": "dev",
    "implementation_plan": "dev",
    "code_skeleton": "dev",
    "test_plan": "qa",
    "coverage_gaps": "qa",
}

NODE_DEPS = {
    "pm": [],
    "arch": ["pm"],
    "dev": ["arch"],
    "qa": ["dev"],
}

NODE_ORDER = ["pm", "arch", "dev", "qa"]


def _normalize_selected_artifacts(selected_artifacts: Iterable[str] | None) -> Set[str]:
    if not selected_artifacts:
        return set(ALL_ARTIFACTS)
    selected = {a for a in selected_artifacts if a in ALL_ARTIFACTS}
    return selected or set(ALL_ARTIFACTS)


def _expand_required_nodes(selected_artifacts: Set[str]) -> Set[str]:
    required = {ARTIFACT_NODE[a] for a in selected_artifacts}
    changed = True
    while changed:
        changed = False
        snapshot = set(required)
        for node in snapshot:
            for dep in NODE_DEPS[node]:
                if dep not in required:
                    required.add(dep)
                    changed = True
    return required


def run(
    idea: str,
    tech_stack: str = "",
    max_loops: int = 2,
    selected_artifacts: Iterable[str] | None = None,
    llm_provider: str | None = None,
    llm_model: str | None = None,
    max_tokens: int = 1_000_000,  # Safety limit per run
    cost_limit_usd: float = 100.0,  # Safety limit on total cost
) -> dict:
    run_dir = make_run_dir()
    llm = build_llm(provider=llm_provider, model_name=llm_model)
    prompts = PromptLibrary(str(Path(__file__).resolve().parent.parent / "prompt-library"))
    selected = _normalize_selected_artifacts(selected_artifacts)
    required_nodes = _expand_required_nodes(selected)

    state = {
        "idea": idea,
        "tech_stack": tech_stack,
        "loop_count": 0,
        "max_loops": max_loops,
        "max_tokens": max_tokens,
        "cost_limit_usd": cost_limit_usd,
        "run_dir": run_dir,
        "node_metrics": {},
        "execution_log": [],
        "total_token_metrics": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "estimated_cost_usd": 0.0,
        },
    }

    if "pm" in required_nodes:
        # Check limits before proceeding
        if not check_cost_limits(state, llm):
            state["last_error"] = f"Cost or token limit exceeded before pm_node"
            write_artifact(run_dir, "00_final_state.json", json.dumps(state, indent=2))
            return state
        
        state = pm_node(state, llm=llm, prompts=prompts, selected_artifacts=selected)
        update_token_metrics(state, llm)

    if "arch" in required_nodes:
        if not check_cost_limits(state, llm):
            state["last_error"] = f"Cost or token limit exceeded before architect_node"
            write_artifact(run_dir, "00_final_state.json", json.dumps(state, indent=2))
            return state
        
        state = architect_node(state, llm=llm, prompts=prompts, selected_artifacts=selected)
        update_token_metrics(state, llm)

    if "dev" in required_nodes:
        if not check_cost_limits(state, llm):
            state["last_error"] = f"Cost or token limit exceeded before developer_node"
            write_artifact(run_dir, "00_final_state.json", json.dumps(state, indent=2))
            return state
        
        state = developer_node(state, llm=llm, prompts=prompts, selected_artifacts=selected)
        update_token_metrics(state, llm)

    if "qa" in required_nodes:
        while True:
            if not check_cost_limits(state, llm):
                state["last_error"] = f"Cost or token limit exceeded in QA loop iteration {state.get('loop_count', 0)}"
                break
            
            state = qa_node(state, llm=llm, prompts=prompts, selected_artifacts=selected)
            update_token_metrics(state, llm)
            
            defects = state.get("defect_list", []) or []
            if not defects:
                break

            if int(state.get("loop_count", 0)) >= max_loops:
                break

            # Loop back: bump loop counter and feed QA defects into dev notes.
            state = {
                **state,
                "loop_count": int(state.get("loop_count", 0)) + 1,
                "dev_notes": f"Fix these defects: {json.dumps(defects, indent=2)}",
                "run_dir": run_dir,
                "max_loops": max_loops,
            }
            state = developer_node(state, llm=llm, prompts=prompts, selected_artifacts=selected)
            update_token_metrics(state, llm)

    write_artifact(run_dir, "00_final_state.json", json.dumps(state, indent=2))
    write_artifact(run_dir, "00_selected_artifacts.json", json.dumps(sorted(selected), indent=2))
    write_artifact(run_dir, "00_executed_nodes.json", json.dumps([n for n in NODE_ORDER if n in required_nodes], indent=2))
    write_artifact(run_dir, "00_token_metrics.json", json.dumps(state.get("total_token_metrics", {}), indent=2))
    write_artifact(run_dir, "00_execution_log.json", json.dumps(state.get("execution_log", []), indent=2))
    write_artifact(run_dir, "00_node_metrics.json", json.dumps(state.get("node_metrics", {}), indent=2))
    
    return state
