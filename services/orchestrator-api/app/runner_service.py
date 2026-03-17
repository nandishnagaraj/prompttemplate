from __future__ import annotations
import sys
from pathlib import Path
from fastapi import HTTPException

ORCH_ROOT = Path(__file__).resolve().parent.parent / "orchestrator_pkg"

def _find_orch_base():
    for p in ORCH_ROOT.rglob("orchestrator"):
        if p.is_dir():
            return p.parent
    return None

_orch_base = _find_orch_base()
if _orch_base is None:
    raise RuntimeError("Bundled orchestrator package not found")
sys.path.insert(0, str(_orch_base))

from orchestrator.runner import run as run_pipeline  # type: ignore

def run_langgraph(
    idea: str,
    tech_stack: str,
    max_loops: int = 2,
    selected_artifacts: list[str] | None = None,
) -> dict:
    try:
        return run_pipeline(
            idea=idea,
            tech_stack=tech_stack,
            max_loops=max_loops,
            selected_artifacts=selected_artifacts,
        )
    except Exception as e:
        raise HTTPException(500, f"Pipeline failed: {e}")
