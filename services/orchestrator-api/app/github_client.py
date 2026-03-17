from __future__ import annotations
import tempfile, shutil
from pathlib import Path
from git import Repo
from git.exc import GitCommandError
from fastapi import HTTPException

def _tokenized_https_url(repo_https_url: str, token: str) -> str:
    if repo_https_url.startswith("https://"):
        return repo_https_url.replace("https://", f"https://x-access-token:{token}@", 1)
    raise HTTPException(400, "Only https repo URLs are supported")

def push_run_folder(*, token: str, repo_https_url: str, branch: str, run_folder: str, dest_subdir: str = "runs") -> str:
    tmp = tempfile.mkdtemp(prefix="repo-")
    try:
        url = _tokenized_https_url(repo_https_url, token)
        try:
            repo = Repo.clone_from(url, tmp, branch=branch)
        except GitCommandError as exc:
            stderr = (exc.stderr or "").strip()
            if "Remote branch" in stderr and "not found" in stderr:
                raise HTTPException(400, f"Branch '{branch}' was not found in the target repository.")
            if "Repository not found" in stderr:
                raise HTTPException(400, "Repository not found or you do not have access with the current GitHub token.")
            if "Authentication failed" in stderr or "could not read Username" in stderr:
                raise HTTPException(401, "GitHub authentication failed while cloning target repository.")
            raise HTTPException(400, f"Failed to clone repository: {stderr or str(exc)}")
        repo_path = Path(tmp)
        run_path = Path(run_folder)
        if not run_path.exists():
            raise HTTPException(500, f"Run folder not found: {run_folder}")

        target = repo_path / dest_subdir / run_path.name
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(run_path, target)

        repo.git.add(A=True)
        if repo.is_dirty():
            repo.index.commit(f"AI: add generated artifacts {run_path.name}")
            try:
                repo.remote("origin").push(refspec=f"{branch}:{branch}")
            except GitCommandError as exc:
                stderr = (exc.stderr or "").strip()
                raise HTTPException(400, f"Failed to push to branch '{branch}': {stderr or str(exc)}")
        return repo.head.commit.hexsha[:7]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
