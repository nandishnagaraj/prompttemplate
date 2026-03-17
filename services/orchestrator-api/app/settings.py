from __future__ import annotations
import os
from pydantic import BaseModel

class Settings(BaseModel):
    github_base_url: str = os.getenv("GITHUB_BASE_URL", "https://github.com").rstrip("/")
    github_client_id: str = os.getenv("GITHUB_CLIENT_ID", "")
    github_client_secret: str = os.getenv("GITHUB_CLIENT_SECRET", "")
    github_redirect_uri: str = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8000/auth/callback").rstrip("/")
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3003").rstrip("/")
    allow_pat_fallback: bool = os.getenv("ALLOW_PAT_FALLBACK", "true").lower() == "true"
    session_secret: str = os.getenv("SESSION_SECRET", "change-me")

    azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    azure_openai_deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")
    azure_openai_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "")

settings = Settings()
