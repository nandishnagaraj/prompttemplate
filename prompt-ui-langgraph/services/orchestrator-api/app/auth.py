from __future__ import annotations
import base64
import hashlib
import hmac
import json
import secrets
import time
from urllib.parse import quote_plus, urlencode
import requests
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from .settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])
_SESSIONS: dict[str, dict] = {}
_OAUTH_STATES: dict[str, dict] = {}
_STATE_MAX_AGE_SECONDS = 600


def _cookie_samesite_value() -> str:
    value = (settings.session_cookie_samesite or "lax").strip().lower()
    if value not in {"lax", "strict", "none"}:
        return "lax"
    return value


def _set_session_cookie(response: RedirectResponse, session_id: str) -> None:
    response.set_cookie(
        "session_id",
        session_id,
        httponly=True,
        samesite=_cookie_samesite_value(),
        secure=bool(settings.session_cookie_secure),
    )


def _set_oauth_state_cookie(response: RedirectResponse, provider: str, state: str) -> None:
    response.set_cookie(
        "oauth_state",
        state,
        httponly=True,
        samesite=_cookie_samesite_value(),
        secure=bool(settings.session_cookie_secure),
        max_age=600,
    )
    response.set_cookie(
        "oauth_provider",
        provider,
        httponly=True,
        samesite=_cookie_samesite_value(),
        secure=bool(settings.session_cookie_secure),
        max_age=600,
    )


def _clear_oauth_state_cookie(response: RedirectResponse) -> None:
    response.delete_cookie("oauth_state")
    response.delete_cookie("oauth_provider")


def _get_session_id(request: Request) -> str | None:
    # Fallback order: cookie -> custom header -> query parameter.
    sid = request.cookies.get("session_id")
    if sid:
        return sid
    sid = request.headers.get("x-session-id")
    if sid:
        return sid
    sid = request.query_params.get("session_id")
    if sid:
        return sid
    return None


def _b64url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode().rstrip("=")


def _b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def _sign_state_payload(payload_b64: str) -> str:
    secret = settings.session_secret.encode()
    return hmac.new(secret, payload_b64.encode(), hashlib.sha256).hexdigest()


def _build_oauth_state(provider: str) -> str:
    payload = {
        "provider": provider,
        "nonce": secrets.token_urlsafe(16),
        "ts": int(time.time()),
    }
    payload_b64 = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    signature = _sign_state_payload(payload_b64)
    return f"{payload_b64}.{signature}"


def _validate_signed_oauth_state(state: str, expected_provider: str) -> bool:
    try:
        payload_b64, signature = state.split(".", 1)
    except ValueError:
        return False

    expected_signature = _sign_state_payload(payload_b64)
    if not hmac.compare_digest(signature, expected_signature):
        return False

    try:
        payload = json.loads(_b64url_decode(payload_b64).decode())
    except Exception:
        return False

    if payload.get("provider") != expected_provider:
        return False

    issued_at = int(payload.get("ts", 0))
    if not issued_at or time.time() - issued_at > _STATE_MAX_AGE_SECONDS:
        return False

    return True


def _is_valid_oauth_state(request: Request, state: str, expected_provider: str) -> bool:
    if _validate_signed_oauth_state(state, expected_provider):
        return True

    data = _OAUTH_STATES.pop(state, None)
    if data and data.get("provider") == expected_provider:
        return True

    # Fallback: validate against cookies in case process restarted between login and callback.
    cookie_state = request.cookies.get("oauth_state", "")
    cookie_provider = request.cookies.get("oauth_provider", "")
    return cookie_state == state and cookie_provider == expected_provider


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
    state = _build_oauth_state(provider)
    _OAUTH_STATES[state] = {"provider": provider}

    if provider == "github":
        if not settings.github_client_id:
            raise HTTPException(500, "GITHUB_CLIENT_ID not set")
        response = RedirectResponse(_github_authorize_url(state))
        _set_oauth_state_cookie(response, provider, state)
        return response

    if provider == "bitbucket":
        if not settings.bitbucket_client_id:
            raise HTTPException(500, "BITBUCKET_CLIENT_ID not set")
        response = RedirectResponse(_bitbucket_authorize_url(state))
        _set_oauth_state_cookie(response, provider, state)
        return response

    raise HTTPException(400, "Unsupported provider. Use 'github' or 'bitbucket'.")

@router.get("/callback")
def callback(code: str, state: str, request: Request):
    if not _is_valid_oauth_state(request, state, "github"):
        raise HTTPException(400, "Invalid or expired OAuth state. Start login again.")
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
    params = urlencode({"git_provider": "github", "session_id": session_id})
    r = RedirectResponse(url=f"{settings.frontend_url}/?{params}")
    _set_session_cookie(r, session_id)
    _clear_oauth_state_cookie(r)
    return r


@router.get("/bitbucket/callback")
def bitbucket_callback(code: str, state: str, request: Request):
    if not _is_valid_oauth_state(request, state, "bitbucket"):
        raise HTTPException(400, "Invalid or expired OAuth state. Start login again.")
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
    body = resp.json()
    tok = body.get("access_token")
    if not tok:
        raise HTTPException(400, f"Bitbucket OAuth failed: {resp.text}")
    refresh_tok = body.get("refresh_token", "")

    session_id = secrets.token_urlsafe(32)
    _SESSIONS[session_id] = {"provider": "bitbucket", "token": tok, "refresh_token": refresh_tok}
    params = urlencode({"git_provider": "bitbucket", "session_id": session_id})
    r = RedirectResponse(url=f"{settings.frontend_url}/?{params}")
    _set_session_cookie(r, session_id)
    _clear_oauth_state_cookie(r)
    return r

@router.post("/logout")
def logout(request: Request):
    sid = _get_session_id(request)
    if sid:
        _SESSIONS.pop(sid, None)
    r = JSONResponse({"ok": True})
    r.delete_cookie("session_id")
    return r


def get_provider_token(request: Request, provider: str) -> str | None:
    sid = _get_session_id(request)
    if sid and sid in _SESSIONS:
        data = _SESSIONS[sid]
        if data.get("provider") == provider:
            return data.get("token")
    return None


def get_provider_refresh_token(request: Request, provider: str) -> str | None:
    sid = _get_session_id(request)
    if sid and sid in _SESSIONS:
        data = _SESSIONS[sid]
        if data.get("provider") == provider:
            return data.get("refresh_token")
    return None


def update_provider_token(request: Request, provider: str, new_access_token: str) -> None:
    """Replace the stored access token after a successful refresh."""
    sid = _get_session_id(request)
    if sid and sid in _SESSIONS and _SESSIONS[sid].get("provider") == provider:
        _SESSIONS[sid]["token"] = new_access_token


def get_session_provider(request: Request) -> str | None:
    sid = _get_session_id(request)
    if sid and sid in _SESSIONS:
        return _SESSIONS[sid].get("provider")
    return None


def get_github_token(request: Request) -> str | None:
    return get_provider_token(request, "github")
