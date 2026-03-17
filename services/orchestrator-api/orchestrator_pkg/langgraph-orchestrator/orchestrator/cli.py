from __future__ import annotations

import argparse
from pathlib import Path

from .llm import build_llm
from .graph import build_graph
from .io_utils import make_run_dir, write_artifact


def main():
    parser = argparse.ArgumentParser(description="LangGraph SDLC orchestrator (PM→Arch→Dev→QA)")
    parser.add_argument("--idea", required=True, help="Business idea / feature description")
    parser.add_argument("--tech_stack", default="", help="Tech stack constraints (e.g., React, Spring Boot, Postgres)")
    parser.add_argument("--max_loops", type=int, default=2, help="Max QA→Dev loop iterations")
    args = parser.parse_args()

    run_dir = make_run_dir()
    llm = build_llm()

    graph = build_graph(llm=llm, prompt_root=str(Path(__file__).resolve().parent.parent / "prompt-library"))

    state = {
        "idea": args.idea,
        "tech_stack": args.tech_stack,
        "loop_count": 0,
        "max_loops": args.max_loops,
        "run_dir": run_dir,
    }

    result = graph.invoke(state)

    # If we looped back, increment loop_count in the state between iterations.
    # Note: in a full implementation with durable execution/checkpointing, you’d persist step-by-step.
    # Here we just show a single-pass invoke. If you want multi-iteration execution, use the runner below.
    write_artifact(run_dir, "00_final_state.json", __import__("json").dumps(result, indent=2))

    print(f"Run complete. Artifacts written to: {run_dir}")
    defects = result.get("defect_list", []) or []
    if defects:
        print(f"Defects detected: {len(defects)} (see 10_test_plan.md / 11_coverage_gaps.md)")
    else:
        print("No defects detected by heuristic extraction.")


if __name__ == "__main__":
    main()
