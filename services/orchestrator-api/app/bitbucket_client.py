from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
import requests
from fastapi import HTTPException


def _parse_bitbucket_repo(repo_https_url: str) -> tuple[str, str]:
    parsed = urlparse(repo_https_url)
    if parsed.scheme != "https":
        raise HTTPException(400, "Only https repo URLs are supported")
    if parsed.netloc.lower() != "bitbucket.org":
        raise HTTPException(400, "Bitbucket provider requires a bitbucket.org repository URL")

    parts = [p for p in parsed.path.strip("/").split("/") if p]
    if len(parts) < 2:
        raise HTTPException(400, "Invalid Bitbucket URL. Expected https://bitbucket.org/<workspace>/<repo>")

    workspace = parts[0]
    repo_slug = parts[1]
    if repo_slug.endswith(".git"):
        repo_slug = repo_slug[:-4]

    return workspace, repo_slug


def push_run_folder(*, token: str, repo_https_url: str, branch: str, run_folder: str, dest_subdir: str = "runs") -> str:
    workspace, repo_slug = _parse_bitbucket_repo(repo_https_url)
    run_path = Path(run_folder)
    if not run_path.exists() or not run_path.is_dir():
        raise HTTPException(500, f"Run folder not found: {run_folder}")

    endpoint = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/src"
    headers = {"Authorization": f"Bearer {token}"}

    files_payload: list[tuple[str, tuple[str, bytes]]] = []
    for file_path in run_path.rglob("*"):
        if not file_path.is_file():
            continue
        rel = file_path.relative_to(run_path).as_posix()
        target_path = f"{dest_subdir}/{run_path.name}/{rel}"
        files_payload.append((target_path, (target_path, file_path.read_bytes())))

    data = {
        "message": f"AI: add generated artifacts {run_path.name}",
        "branch": branch,
    }

    resp = requests.post(endpoint, headers=headers, data=data, files=files_payload, timeout=120)
    if resp.status_code >= 400:
        detail = ""
        try:
            detail = resp.json().get("error", {}).get("message", "")
        except Exception:
            detail = resp.text

        if resp.status_code in {401, 403}:
            raise HTTPException(401, f"Bitbucket authentication failed: {detail or 'unauthorized'}")
        if resp.status_code == 404:
            raise HTTPException(400, "Bitbucket repository or branch not found, or no access")
        raise HTTPException(400, f"Failed to push to Bitbucket: {detail or resp.text}")

    payload = resp.json() if resp.content else {}
    commit_hash = payload.get("commit", {}).get("hash", "")
    return (commit_hash[:7] if commit_hash else "unknown")
