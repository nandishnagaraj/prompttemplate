from __future__ import annotations
import secrets
from urllib.parse import quote_plus
import requests
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from .settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])
_SESSIONS: dict[str, dict] = {}
_OAUTH_STATES: dict[str, dict] = {}


def _github_authorize_url(state: str) -> str:
    return (
        f"{settings.github_base_url}/login/oauth/authorize"
        f"?client_id={settings.github_client_id}"
        f"&redirect_uri={settings.github_redirect_uri}"
        f"&state={state}"
        f"&scope=repo"
    )


def _bitbucket_authorize_url(state: str) -> str:
    return (
        "https://bitbucket.org/site/oauth2/authorize"
        f"?client_id={settings.bitbucket_client_id}"
        "&response_type=code"
        f"&redirect_uri={quote_plus(settings.bitbucket_redirect_uri)}"
        f"&state={state}"
    )

@router.get("/login")
def login(provider: str = "github"):
    provider = provider.strip().lower()
    state = secrets.token_urlsafe(24)
    _OAUTH_STATES[state] = {"provider": provider}

    if provider == "github":
        if not settings.github_client_id:
            raise HTTPException(500, "GITHUB_CLIENT_ID not set")
        return RedirectResponse(_github_authorize_url(state))

    if provider == "bitbucket":
        if not settings.bitbucket_client_id:
            raise HTTPException(500, "BITBUCKET_CLIENT_ID not set")
        return RedirectResponse(_bitbucket_authorize_url(state))

    raise HTTPException(400, "Unsupported provider. Use 'github' or 'bitbucket'.")

@router.get("/callback")
def callback(code: str, state: str, request: Request):
    data = _OAUTH_STATES.pop(state, None)
    if not data or data.get("provider") != "github":
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
    try:
        resp = requests.post(token_url, data=data, headers=headers, timeout=30)
        resp.raise_for_status()
    except requests.HTTPError:
        detail = ""
        try:
            detail = resp.json().get("error_description") or resp.json().get("error") or resp.text
        except Exception:
            detail = resp.text if "resp" in locals() else ""
        raise HTTPException(400, f"GitHub OAuth token exchange failed: {detail or 'bad request'}")
    except requests.RequestException as e:
        raise HTTPException(502, f"GitHub OAuth network error: {e}")
    tok = resp.json().get("access_token")
    if not tok:
        raise HTTPException(400, f"OAuth failed: {resp.text}")

    session_id = secrets.token_urlsafe(32)
    _SESSIONS[session_id] = {"provider": "github", "token": tok}
    r = RedirectResponse(url=f"{settings.frontend_url}/?git_provider=github")
    r.set_cookie("session_id", session_id, httponly=True, samesite="lax")
    return r


@router.get("/bitbucket/callback")
def bitbucket_callback(code: str, state: str):
    data = _OAUTH_STATES.pop(state, None)
    if not data or data.get("provider") != "bitbucket":
        raise HTTPException(400, "Invalid state")
    if not settings.bitbucket_client_secret:
        raise HTTPException(500, "BITBUCKET_CLIENT_SECRET not set")

    token_url = "https://bitbucket.org/site/oauth2/access_token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.bitbucket_redirect_uri,
    }
    headers = {"Accept": "application/json"}
    try:
        resp = requests.post(
            token_url,
            data=payload,
            headers=headers,
            auth=(settings.bitbucket_client_id, settings.bitbucket_client_secret),
            timeout=30,
        )
        resp.raise_for_status()
    except requests.HTTPError:
        detail = ""
        try:
            data = resp.json()
            detail = data.get("error_description") or data.get("error") or data.get("message") or resp.text
        except Exception:
            detail = resp.text if "resp" in locals() else ""
        raise HTTPException(400, f"Bitbucket OAuth token exchange failed: {detail or 'bad request'}")
    except requests.RequestException as e:
        raise HTTPException(502, f"Bitbucket OAuth network error: {e}")
    tok = resp.json().get("access_token")
    if not tok:
        raise HTTPException(400, f"Bitbucket OAuth failed: {resp.text}")

    session_id = secrets.token_urlsafe(32)
    _SESSIONS[session_id] = {"provider": "bitbucket", "token": tok}
    r = RedirectResponse(url=f"{settings.frontend_url}/?git_provider=bitbucket")
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


def get_provider_token(request: Request, provider: str) -> str | None:
    sid = request.cookies.get("session_id")
    if sid and sid in _SESSIONS:
        data = _SESSIONS[sid]
        if data.get("provider") == provider:
            return data.get("token")
    return None


def get_session_provider(request: Request) -> str | None:
    sid = request.cookies.get("session_id")
    if sid and sid in _SESSIONS:
        return _SESSIONS[sid].get("provider")
    return None


def get_github_token(request: Request) -> str | None:
    return get_provider_token(request, "github")
