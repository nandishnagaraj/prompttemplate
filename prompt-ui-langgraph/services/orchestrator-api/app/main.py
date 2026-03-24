from __future__ import annotations
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .auth import router as auth_router, get_provider_token, get_provider_refresh_token, update_provider_token, get_session_provider
from .settings import settings
from .runner_service import run_langgraph
from .github_client import push_run_folder as push_run_folder_github
from .bitbucket_client import push_run_folder as push_run_folder_bitbucket

app = FastAPI(title="Prompt UI Orchestrator API", version="0.1.0")

allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3003",
    "http://localhost:3004",
    "http://localhost:3005",
    settings.frontend_url,
]

allowed_origins = list(dict.fromkeys(allowed_origins))

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
    git_provider: str = Field(default="github")
    llm_provider: str = Field(default="azure")
    llm_model: str = Field(default="")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/me")
def me(request: Request, provider: str = "github"):
    selected_provider = provider.strip().lower()
    if selected_provider not in {"github", "bitbucket"}:
        raise HTTPException(400, "Unsupported provider. Use 'github' or 'bitbucket'.")
    return {
        "authenticated": bool(get_provider_token(request, selected_provider)),
        "provider": get_session_provider(request),
    }

@app.post("/runs")
def run_and_push(req: RunRequest, request: Request):
    selected_provider = req.git_provider.strip().lower()
    if selected_provider not in {"github", "bitbucket"}:
        raise HTTPException(400, "Unsupported git provider. Use 'github' or 'bitbucket'.")

    token = get_provider_token(request, selected_provider)
    if not token:
        raise HTTPException(401, f"Not authenticated for {selected_provider}. Use /auth/login?provider={selected_provider} first.")

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

    if selected_provider == "github":
        sha = push_run_folder_github(
            token=token,
            repo_https_url=req.repo_https_url,
            branch=req.branch,
            run_folder=str(latest),
            dest_subdir=req.dest_subdir,
        )
    else:
        refresh_tok = get_provider_refresh_token(request, "bitbucket")
        sha, active_token = push_run_folder_bitbucket(
            token=token,
            repo_https_url=req.repo_https_url,
            branch=req.branch,
            run_folder=str(latest),
            dest_subdir=req.dest_subdir,
            refresh_token=refresh_tok,
            client_id=settings.bitbucket_client_id,
            client_secret=settings.bitbucket_client_secret,
        )
        # Persist the (possibly refreshed) access token back to the session
        if active_token and active_token != token:
            update_provider_token(request, "bitbucket", active_token)

    return {
        "run_folder": latest.name,
        "commit": sha,
        "repo": req.repo_https_url,
        "branch": req.branch,
        "git_provider": selected_provider,
        "files": [p.name for p in latest.iterdir() if p.is_file()],
    }
