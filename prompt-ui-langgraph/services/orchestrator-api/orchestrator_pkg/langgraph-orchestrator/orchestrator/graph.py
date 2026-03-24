from __future__ import annotations

from typing import Literal, Any

from langgraph.graph import StateGraph, START, END
from langgraph.types import RetryPolicy

from .state import OrchestratorState
from .nodes import pm_node, architect_node, developer_node, qa_node
from .prompts import PromptLibrary


def _route_after_qa(state: OrchestratorState) -> Literal["dev", "end"]:
    defects = state.get("defect_list", []) or []
    loop_count = int(state.get("loop_count", 0) or 0)
    max_loops = int(state.get("max_loops", 2) or 2)

    # If we have defects and haven't exceeded loops, go back to dev
    if defects and loop_count < max_loops:
        return "dev"
    return "end"


def build_graph(*, llm: Any, prompt_root: str) -> Any:
    prompts = PromptLibrary(prompt_root)

    builder = StateGraph(OrchestratorState)

    # Retry policies on nodes that call external services (LLM)
    default_retry = RetryPolicy(max_attempts=3)

    builder.add_node("pm", lambda s: pm_node(s, llm=llm, prompts=prompts), retry_policy=default_retry)
    builder.add_node("arch", lambda s: architect_node(s, llm=llm, prompts=prompts), retry_policy=default_retry)
    builder.add_node("dev", lambda s: developer_node(s, llm=llm, prompts=prompts), retry_policy=default_retry)
    builder.add_node("qa", lambda s: qa_node(s, llm=llm, prompts=prompts), retry_policy=default_retry)

    # Linear flow
    builder.add_edge(START, "pm")
    builder.add_edge("pm", "arch")
    builder.add_edge("arch", "dev")
    builder.add_edge("dev", "qa")

    # Conditional: QA loops back to Dev if defects found (bounded by max_loops)
    builder.add_conditional_edges("qa", _route_after_qa, {"dev": "dev", "end": END})

    graph = builder.compile()
    return graph
