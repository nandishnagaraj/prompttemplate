from __future__ import annotations
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .auth import router as auth_router, get_github_token
from .settings import settings
from .runner_service import run_langgraph
from .github_client import push_run_folder

app = FastAPI(title="Prompt UI Orchestrator API", version="0.1.0")

allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3003",
    "http://localhost:3004",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

class RunRequest(BaseModel):
    idea: str = Field(..., min_length=5)
    tech_stack: str = Field(default="")
    repo_https_url: str = Field(...)
    branch: str = Field(default="main")
    max_loops: int = Field(default=2, ge=0, le=5)
    dest_subdir: str = Field(default="runs")
    role: str = Field(default="custom")
    selected_artifacts: list[str] = Field(default_factory=list)
    llm_provider: str = Field(default="azure")
    llm_model: str = Field(default="")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/me")
def me(request: Request):
    return {"authenticated": bool(get_github_token(request))}

@app.post("/runs")
def run_and_push(req: RunRequest, request: Request):
    token = get_github_token(request)
    if not token:
        raise HTTPException(401, "Not authenticated. Use /auth/login first.")

    _ = run_langgraph(
        req.idea,
        req.tech_stack,
        req.max_loops,
        selected_artifacts=req.selected_artifacts,
        llm_provider=req.llm_provider,
        llm_model=req.llm_model or None,
    )

    runs_dir = Path("runs")
    if not runs_dir.exists():
        raise HTTPException(500, "runs/ folder not found after execution")

    latest = max([p for p in runs_dir.iterdir() if p.is_dir()], key=lambda p: p.stat().st_mtime, default=None)
    if latest is None:
        raise HTTPException(500, "No run folder created")

    sha = push_run_folder(token=token, repo_https_url=req.repo_https_url, branch=req.branch, run_folder=str(latest), dest_subdir=req.dest_subdir)

    return {
        "run_folder": latest.name,
        "commit": sha,
        "repo": req.repo_https_url,
        "branch": req.branch,
        "files": [p.name for p in latest.iterdir() if p.is_file()],
    }
