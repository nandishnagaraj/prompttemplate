# LangGraph Multi-Agent Orchestrator (PM → Architect → Dev → QA)

Push-button SDLC automation using **LangGraph StateGraph** with:
- Shared state object
- Node-level retry policies
- QA→Dev loopback with max-iteration guard
- Prompt templates loaded from `prompt-library/` (your 33 templates)

Generated: 2026-02-22

## Quickstart

### 1) Install
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Configure LLM (choose one)

**Option A — OpenAI / compatible**
```bash
export OPENAI_API_KEY="..."
export MODEL_NAME="gpt-4.1-mini"
```

**Option B — Azure OpenAI (example)**
```bash
export AZURE_OPENAI_API_KEY="..."
export AZURE_OPENAI_ENDPOINT="https://<resource>.openai.azure.com/"
export AZURE_OPENAI_DEPLOYMENT="<deployment_name>"
```

If no keys are set, the orchestrator falls back to a deterministic **MockLLM** (useful for wiring/testing).

### 3) Run
```bash
python -m orchestrator.cli --idea "Build a leave management system" --tech_stack "React, Node.js, PostgreSQL"
```

Outputs are written to `runs/<timestamp>/` as markdown artifacts.

## What it does

1. PM node generates PRD + RTM using templates under `prompt-library/01-prd/`.
2. Architect node generates architecture + ADRs + risk review using `prompt-library/03-design/`.
3. Developer node generates user stories (if missing), and an implementation plan.
4. QA node generates test plan and checks for coverage/defects.
5. If defects found, graph loops back to Developer (max loops configurable).

## Notes

- **Retry policies** are configured per-node via `RetryPolicy(...)` as documented by LangGraph. citeturn2view1
- Graph construction uses `StateGraph`, `add_node`, `add_edge`, `add_conditional_edges`, `compile()`. citeturn1view1turn1view0
