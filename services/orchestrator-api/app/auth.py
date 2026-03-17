from __future__ import annotations
import secrets
import requests
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from .settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])
_SESSIONS: dict[str, dict] = {}

def _authorize_url(state: str) -> str:
    return (
        f"{settings.github_base_url}/login/oauth/authorize"
        f"?client_id={settings.github_client_id}"
        f"&redirect_uri={settings.github_redirect_uri}"
        f"&state={state}"
        f"&scope=repo"
    )

@router.get("/login")
def login():
    if not settings.github_client_id:
        raise HTTPException(500, "GITHUB_CLIENT_ID not set")
    state = secrets.token_urlsafe(24)
    _SESSIONS[state] = {"created": True}
    return RedirectResponse(_authorize_url(state))

@router.get("/callback")
def callback(code: str, state: str, request: Request):
    if state not in _SESSIONS:
        raise HTTPException(400, "Invalid state")
    if not settings.github_client_secret:
        raise HTTPException(500, "GITHUB_CLIENT_SECRET not set")

    token_url = f"{settings.github_base_url}/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    data = {
        "client_id": settings.github_client_id,
        "client_secret": settings.github_client_secret,
        "code": code,
        "state": state,
        "redirect_uri": settings.github_redirect_uri,
    }
    resp = requests.post(token_url, data=data, headers=headers, timeout=30)
    resp.raise_for_status()
    tok = resp.json().get("access_token")
    if not tok:
        raise HTTPException(400, f"OAuth failed: {resp.text}")

    session_id = secrets.token_urlsafe(32)
    _SESSIONS[session_id] = {"token": tok}
    r = RedirectResponse(url=settings.frontend_url)
    r.set_cookie("session_id", session_id, httponly=True, samesite="lax")
    return r

@router.post("/logout")
def logout(request: Request):
    sid = request.cookies.get("session_id")
    if sid:
        _SESSIONS.pop(sid, None)
    r = JSONResponse({"ok": True})
    r.delete_cookie("session_id")
    return r

def get_github_token(request: Request) -> str | None:
    sid = request.cookies.get("session_id")
    if sid and sid in _SESSIONS:
        return _SESSIONS[sid].get("token")
    return None
